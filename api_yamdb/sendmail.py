from django.core.mail import  EmailMessage
from django.http import HttpResponse


def send_message(request):
    if request.method == 'GET':
        em = EmailMessage(
            subject='Олега атата',
            body='Тут в будущем будет confrom code',
            to=['okodit@yandex.ru', 'stupid_face@mail.ru'],
        )
        em.send()
        return HttpResponse(em)
