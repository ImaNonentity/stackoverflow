from django.core.mail import send_mail
from django.http import HttpResponse


def sendmail(request):
    send_mail(
        'Hey there :)',
        'Have a great day!',
        'stackoverflow@test.com',
        ['childmoon11@gmail.com'],
        fail_silently=False,
    )

    return HttpResponse('Mail successfully sent!')
