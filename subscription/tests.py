from django.urls import reverse
from rest_framework import test, status

from materials.models import Course, Lesson
from subscription.models import Subscription
from users.models import User


class SubscriptionTestCase(test.APITestCase):
    """ Тест функционала работы подписки на курс. """

    def setUp(self):
        self.user = User.objects.create(email='test@test.test')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(owner=self.user, name='курс', description='описание курса')
        self.lesson = Lesson.objects.create(owner=self.user, name='урок', description='описание урока',
                                            url='https://youtube.com/', course=self.course)

    def test_subscription_status(self):
        url = reverse('subscription:subscription_status')
        data = {'owner': self.user.pk, 'course': self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 1)  # тест на кол-во в БД
        self.assertEqual(data.get('message'), 'подписка добавлена')  # ожидаемый результат добавления подписки

    def test_subscription_status_2(self):
        url = reverse('subscription:subscription_status')
        data = {'owner': self.user.pk, 'course': self.course.pk}
        self.client.post(url, data)  # делаем 2 поста подряд для проверки на "unsub"
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 0)
        self.assertEqual(data.get('message'), 'подписка удалена')
