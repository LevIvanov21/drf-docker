from django.db import models

from config import settings
from materials.models import Course

NULLABLE = {'blank': True, 'null': True}


class Subscription(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    is_subscribed = models.BooleanField(default=False, verbose_name='наличие подписки', **NULLABLE)

    def __str__(self):
        return f'{self.user} подписка на {self.course.name}: {self.is_subscribed}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
