from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from materials.models import Lesson, Course


class LessonTestCase(APITestCase):
    """ Тестирование CRUD для модели Lesson. """

    def setUp(self):
        """ Создание пользователя, курса и урока для тестирования """
        self.user = User.objects.create(email='test@test.test')
        self.course = Course.objects.create(name='CourseTest1', description='CourseTest1 description',
                                            owner=self.user)
        self.lesson = Lesson.objects.create(name='LessonTest1', description='LessonTest1 description',
                                            course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)  # force_authenticate нужен потому что мы используем токены

    def test_lesson_retrieve(self):
        # мы тестируем запрос, по этому нам нужно его описать
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        # ответ на запрос
        response = self.client.get(url)
        data = response.json()  # нужно для сравнения результатов
        # сравнение ответа на запрос по статус коду
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # сравнение имени объекта модели Lesson
        self.assertEqual(data['name'], self.lesson.name)

    def test_create_lesson(self):
        url = reverse('materials:lessons_create')
        # данные для создания в формате json
        data = {
            'name': 'LessonTest2',
            'description': 'LessonTest2 description',
            'url': 'https://www.youtube.com/test2/',
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # проверяем кол-во в БД, на данный момент у нас есть 1 экземпляр в setUp и второй мы создали, ожидаем ответ 2
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            'name': 'LessonTest3'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], 'LessonTest3')

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        url = reverse('materials:lessons_list')
        response = self.client.get(url)
        data = response.json()
        result = {'count': 1, 'next': None, 'previous': None, 'results': [
            {'id': self.lesson.pk, 'name': self.lesson.name, 'image': None, 'description': self.lesson.description,
             'url': None, 'course': self.course.pk, 'owner': self.user.pk}]}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
