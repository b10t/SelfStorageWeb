from email.policy import default

from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand


def send_email_of_rent():
    # subject_message = 'Вы успешно зарегестрированы на CakeBake'
    # message = f'''
    #         Чтобы войти пройдите по ссылке: https://{current_site.domain}/users/login/
    #         Ваш логин: {email}
    #         Ваш пароль: {password}
    #         '''
    # EmailMessage(
    #     subject=subject_message,
    #     body=message,
    #     to=[email],
    # ).send()

    pass


class Command(BaseCommand):
    help = "Send email of rent."

    def handle(self, *args, **options):
        print('send email')
