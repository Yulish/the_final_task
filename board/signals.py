
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.dispatch import receiver
from .models import Response



@receiver(post_save, sender=Response)
def notify_about_response(sender, instance, created, **kwargs):
    print("Signal fired!")
    if created:
        message = instance.response
        mail = instance.receiver.email
        send_mail(
            subject=str(instance),  # возвращает def_str из модели
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[mail],
            fail_silently=False

        )
@receiver(post_save, sender=Response)
def notify_about_accepted_response(sender, instance, created, **kwargs):
    receiver =instance.receiver.username
    status = instance.status
    if status:
        mail = instance.sender.email
        send_mail(
            subject= "Ваш отклик принят",
            message= f'Ваш отклик {instance.response} от {instance.response_origin.strftime("%d.%m.%Y")} был принят {receiver}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[mail],
            fail_silently=False

        )








