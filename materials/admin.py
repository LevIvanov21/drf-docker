from django.contrib import admin

from materials.models import Lesson, Course


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
