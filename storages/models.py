from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomManager(BaseUserManager):

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Должна быть электронная почта')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        return self._create_user(email, username, password, **extra_fields)


class AdvUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(verbose_name='имя', max_length=150)

    is_staff = models.BooleanField(_('staff status'), default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True)
    objects = CustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return f'{self.username}, {self.email if self.email else "no email"}'

    def get_full_name(self):
        return f'{self.username}, {self.email if self.email else "no email"}'

    def get_short_name(self):
        return self.username


class City(models.Model):
    city = models.CharField('Город', max_length=50)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.city


class Storage(models.Model):
    address = models.CharField('Адрес', max_length=50)
    temperature = models.SmallIntegerField('Температура на складе')
    max_height = models.DecimalField(
        'Максимальная высота потолка',
        decimal_places=2,
        max_digits=5,
    )
    description = models.TextField(
        'Описание',
        blank=True,
        default='',
    )
    driving_instructions = models.TextField(
        'Как проехать',
        blank=True,
        default='',
    )
    city = models.ForeignKey(
        City,
        verbose_name='Город',
        related_name='storages',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f'{self.city}, {self.address}'


class Box(models.Model):
    storage = models.ForeignKey(
        Storage,
        verbose_name='Склад',
        related_name='boxes_in_storage',
        on_delete=models.CASCADE,
    )
    length = models.DecimalField(
        'Длина',
        decimal_places=2,
        max_digits=5,
    )
    width = models.DecimalField(
        'Ширина',
        decimal_places=2,
        max_digits=5,
    )
    total_area = models.DecimalField(
        'Общая площадь (заполняется автоматически)',
        decimal_places=2,
        max_digits=5,
        blank=True,
    )
    height = models.DecimalField(
        'Высота',
        decimal_places=2,
        max_digits=5,
        blank=True
    )

    is_available = models.BooleanField('Свободен', default=True)
    cost = models.PositiveSmallIntegerField('Стоимость')

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def save(self, *args, **kwargs):
        if not self.height:
            self.height = self.storage.max_height
        if not self.total_area:
            self.total_area = self.width * self.length
        super(Box, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.storage}: {round((self.length * self.width), 2)} м.кв.'


class Image(models.Model):
    storage = models.ForeignKey(
        Storage,
        verbose_name='Фото склада',
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = models.ImageField('Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'{self.pk} - {self.storage.address}'
