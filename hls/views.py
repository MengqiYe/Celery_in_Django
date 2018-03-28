from django.core.mail import send_mail
from django.shortcuts import render

from hls.camera import VideoCamera
from hls.tasks import task_frame_process


# Create your views here.

def dashboard(request):
    return render(request,
                  'hls/dashboard.html')


def task_use_celery(request):
    vc = VideoCamera()
    task_frame_process.delay(vc)
    return render(request,
                  'process_done.html')


def task_not_use_celery(request):
    subject = 'subject test'
    message = 'message test'
    recipient = [
        'sevenseaswander@gmail.com',
        'sevenseaswander@gmail.com',
        'sevenseaswander@gmail.com'
    ]
    send_mail(subject,
              message,
              'taigasupport@yungoal.com',
              recipient)
    return render(request,
                  'process_done.html')
