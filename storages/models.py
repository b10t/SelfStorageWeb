from django.db import models


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
    height = models.DecimalField(
        'Высота потолка',
        decimal_places=2,
        max_digits=5,
    )
    description = models.TextField(
        'Описание',
        blank=True,
        default='',
    )
    driving_instructions = models.TextField(
        'Проезд',
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
    space = models.PositiveSmallIntegerField('Площадь')
    is_available = models.BooleanField('Доступность', default=True)
    cost = models.PositiveSmallIntegerField('Стоимость')

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return f'{self.storage}: {self.space} м.кв.'


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
