from django.conf import settings
from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    """Модель курса"""
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец',
                              **NULLABLE)
    name = models.CharField(max_length=100, verbose_name='название курса', help_text='введите название курса')
    description = models.TextField(verbose_name='описание курса', help_text='введите описание курса', **NULLABLE)
    image = models.ImageField(upload_to='materials/course', verbose_name='изображение',
                              help_text='выберите изображение', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='стоимость курса', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='дата создания', **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='дата обновления', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """Модель урока, параметр url это ссылка на видео урока"""
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец',
                              **NULLABLE)
    name = models.CharField(max_length=100, verbose_name='название урока', help_text='введите название')
    description = models.TextField(verbose_name='описание урока', help_text='введите описание', **NULLABLE)
    image = models.ImageField(upload_to='materials/lesson', verbose_name='изображение',
                              help_text='выберите изображение', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson_set', verbose_name='курс',
                               help_text='выберите курс')
    url = models.URLField(verbose_name='ссылка', help_text='добавьте ссылку', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='стоимость урока', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='дата создания', **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='дата обновления', **NULLABLE)

    def __str__(self):
        return f"{self.name}, курс {self.course}"

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
