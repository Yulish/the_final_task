import datetime
import logging
from sched import scheduler
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from board.models import Poster

logger = logging.getLogger(__name__)

users = User.objects.all()
email_list = list(users.values_list('email', flat=True))

def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posters = Poster.objects.filter(poster_origin__gte=last_week)
    html_content = render_to_string(
        'weekly_posters.html',
        {
            'link': settings.SITE_URL,
            'posters': posters,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новые публикации за неделю:',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email_list,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="09", minute="00"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
        scheduler.start()

        import time
        while True:
            time.sleep(1)

