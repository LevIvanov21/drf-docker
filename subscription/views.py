from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from materials.models import Course
from subscription.models import Subscription
from subscription.serializers import SubscriptionSerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        """ Переопределение метода для создания и удаления подписки в зависимости от её статуса. """
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        # создание и удаление подписки
        subscription, created = Subscription.objects.get_or_create(user=user, course=course_item, is_subscribed=True)
        if not created:
            subscription.delete()
            message = 'подписка удалена'
        else:
            message = 'подписка добавлена'
        return Response({"message": message})
        # другой вариант
        # subscription = Subscription.objects.filter(user=user, course=course_item, is_subscribed=True)
        # if subscription.exists():
        #     subscription.delete()
        #     message = 'подписка удалена'
        # else:
        #     Subscription.objects.create(user=user, course=course_item, is_subscribed=True)
        #     message = 'подписка добавлена'
        # return Response({"message": message})
