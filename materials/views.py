from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from materials.paginators import CustomPaginator
from materials.permissions import IsModerator, IsOwner

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from materials.tasks import send_updates


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator"
))  # тестовое значение для кастомизации документации
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPaginator

    def perform_create(self, serializer):
        """ Привязывает курс к пользователю при создании. """
        instance = serializer.save()
        instance.owner = self.request.user
        instance.save()

    def perform_update(self, serializer):
        """ Запускает send_updates при редактировании курса. """
        instance = serializer.save()
        send_updates.delay(instance.pk)
        instance.save()

    def get_permissions(self):
        """ Настройка прав для ViewSet. """
        if self.action in ['update', 'partial_update', 'list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'create':
            self.permission_classes = [~IsModerator, IsAuthenticated]
        elif self.action == 'destroy':
            self.permission_classes = [~IsModerator | IsOwner]
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]

    def perform_create(self, serializer):
        """ Привязывает урок к пользователю при создании. """
        instance = serializer.save()
        instance.owner = self.request.user
        instance.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = CustomPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]
