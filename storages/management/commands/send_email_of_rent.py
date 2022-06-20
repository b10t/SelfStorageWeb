from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from storages.models import Rent


def send_email_of_rent(rent, auth_user, auth_password):
    subject_message = 'У вас заканчивается срок аренды!'
    message = f'''
            Добрый день.

            У Вас заканчивается срок аренды бокса:

            Город: {rent.box.storage.city}
            Адрес: {rent.box.storage.address}
            № бокса: {rent.box.number}
            '''
    send_mail(
        subject=subject_message,
        message=message,
        recipient_list=[rent.tenant.email],
        from_email=auth_user,
        auth_user=auth_user,
        auth_password=auth_password
    )


class Command(BaseCommand):
    help = "Send email of rent."

    def handle(self, *args, **options):
        auth_user = settings.EMAIL_HOST_USER
        auth_password = settings.EMAIL_HOST_PASSWORD

        for rent in Rent.objects.all():
            send_email_of_rent(
                rent,
                auth_user,
                auth_password
            )
