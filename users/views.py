from datetime import datetime

import pytz
from django.views.generic import DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from config import settings
from materials.models import Course, Lesson
from users.models import User, Payment
from users.permissions import IsUser
from users.serializers import UserSerializer, PaymentSerializer, UserViewSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session, checkout_session


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """ Хеширование пароля. Переопределение ласт логина нужно для отложенных задач. """
        instance = serializer.save(is_active=True)
        instance.set_password(instance.password)
        instance.last_login = datetime.now(pytz.timezone(settings.TIME_ZONE))
        instance.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUser]

    def perform_update(self, serializer):
        """ Хеширование пароля при редактировании. """
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserViewSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        """ Проверка на владельца профиля. """
        if self.request.user.email == self.get_object().email:
            return UserSerializer
        else:
            return UserViewSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUser]


# class UserViewSet(ModelViewSet):
#     """Реализация через ViewSet"""
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """ Привязывает платеж к пользователю при создании. """
        instance = serializer.save()
        instance.user = self.request.user

        course_id = self.request.data.get('paid_course')
        lesson_id = self.request.data.get('paid_lesson')
        if course_id:
            course_product = create_stripe_product(Course.objects.get(pk=course_id).name)
            course_price = create_stripe_price(instance.paid_course.amount, course_product)
            session_id, payment_link = create_stripe_session(course_price, instance.pk)
        else:
            lesson_product = create_stripe_product(Lesson.objects.get(pk=lesson_id).name)
            lesson_price = create_stripe_price(instance.paid_lesson.amount, lesson_product)
            session_id, payment_link = create_stripe_session(lesson_price, instance.pk)

        payment_status = checkout_session(session_id)
        instance.payment_status = payment_status
        instance.session_id = session_id
        instance.payment_link = payment_link
        instance.save()


class PaymentDetailView(DetailView):
    """ Данные по оплате для success url по её завершению. """
    model = Payment
