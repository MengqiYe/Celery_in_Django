from __future__ import absolute_import, unicode_literals

from celery.schedules import crontab
from celery.task import periodic_task, task
from celery import shared_task
from django.core.mail import send_mail


@task(name="sum_of_two_numbers", ignore_result=True)
def sum_of_two_numbers(num1, num2):
    return num1 + num2


# create task which will run at scheduled time
@periodic_task(run_every=(crontab(minute=0, hour=0)), name="execute_midnight", ignore_result=True)
def execute_midnight():
    # write your code here
    return


@shared_task
def task_mail():
    subject = 'subject test using celery'
    message = 'message test using celery'
    mail_sent = send_mail(subject,
                          message,
                          'taigasupport@yungoal.com',
                          ['sevenseaswander@gmail.com',
                           'sevenseaswander@gmail.com',
                           'sevenseaswander@gmail.com'])
    return mail_sent

@shared_task
def task_frame_process(vc):
    vc.get_frame(vc.video.read())