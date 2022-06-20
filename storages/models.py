import datetime
import uuid

from accounts.models import CustomUser as User
from django.db import models


def now_plus_30():
    """Прибавляет к текущей дате 30 дней."""
    return datetime.datetime.now() + datetime.timedelta(days=30)


class City(models.Model):
    city = models.CharField('Город', max_length=50)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.city


class StorageProperty(models.Model):
    property = models.CharField('Свойство склада', max_length=200)

    class Meta:
        verbose_name = 'Свойство склада'
        verbose_name_plural = 'Свойства склада'


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

    property = models.ForeignKey(
        StorageProperty,
        verbose_name='Свойство',
        related_name='storages',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
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
    number = models.CharField(
        max_length=10,
        verbose_name='№ бокса'
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
        return f'{self.storage}: №{self.number} ({round((self.length * self.width), 2)} м.кв.)'


class Image(models.Model):
    storage = models.ForeignKey(
        Storage,
        verbose_name='Фото склада',
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = models.ImageField('Изображение', upload_to='storage')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'{self.pk} - {self.storage.address}'


class Rent(models.Model):
    """Аренда."""
    tenant = models.ForeignKey(
        User,
        related_name='rents',
        on_delete=models.CASCADE,
        verbose_name='Арендатор',
    )
    box = models.ForeignKey(
        Box,
        related_name='rents',
        on_delete=models.DO_NOTHING,
        verbose_name='Бокс',
    )
    start_rental_period = models.DateField(
        default=datetime.datetime.now,
        verbose_name='Начало аренды'
    )
    end_rental_period = models.DateField(
        default=now_plus_30,
        verbose_name='Окончание аренды'
    )
    payment_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        verbose_name='Идентификатор платежа'
    )
    stripe_payment_id = models.CharField(
        max_length=100,
        blank=True,
        default='',
        editable=False,
        verbose_name='Ид. платежа stripe'
    )
    is_payment = models.BooleanField(
        default=False,
        verbose_name='Оплачен'
    )

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренда'

    def __str__(self):
        return f'{self.pk} - {self.tenant}'
