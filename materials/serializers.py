from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from materials.validators import UrlValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(field='url')]


class CourseSerializer(ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, instance):
        """ Возвращает количество уроков в курсе. """
        return instance.lesson_set.count()

    def get_subscriptions(self, obj):
        """ Возвращает статус подписки пользователя на курс. """
        request = self.context.get('request')
        user = request.user
        if obj.subscription_set.filter(user=user, is_subscribed=True):
            return 'подписка оформлена'
        else:
            return 'подписка отсутствует'
    # другой вариант через инстанс и проверку пользователя, не стал использовать,
    # потому что такие проверки есть на других уровнях
    # def get_subscription(self, instance):
    #     request = self.context.get('request')
    #     user = None
    #     if request:
    #         user = request.user
    #     return instance.subscription_set.filter(user=user).exists()
