import smtplib

from celery import shared_task
from django.core.mail import send_mail

from config import settings
from materials.models import Course
from users.models import User


@shared_task
def send_updates(pk):
    """ При обновлении курса отправляет письмо пользователю, подписанному на курс. """
    instance = Course.objects.filter(pk=pk).first()

    if instance:
        subscribers = instance.subscription_set.filter(is_subscribed=True)
        subscribers_email = []
        for subscriber in subscribers:
            subscribers_email.append(User.objects.get(pk=subscriber.user.pk).email)

        if instance.updated_at > instance.created_at:
            try:
                send_mail(
                    subject='Обновление курса',
                    message=f'Материалы курса {instance.name} обновлены.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=subscribers_email,
                    fail_silently=False
                )
            except smtplib.SMTPException as error:
                raise error
