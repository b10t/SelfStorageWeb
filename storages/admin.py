from django.contrib import admin
from django.utils.html import format_html

from .models import Box, City, Image, Rent, Storage, StorageProperty


class ImageInLine(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ("get_preview", )

    def get_preview(self, obj):
        return format_html(
            f'<img src="{obj.image.url}" width="200" />'
        )


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('storage', 'number', 'length', 'width',
                    'total_area', 'cost', 'is_available')
    fields = ('storage', 'number', 'length', 'width',
              'cost', 'is_available')


@admin.register(StorageProperty)
class StoragePropertyAdmin(admin.ModelAdmin):
    pass

class BoxInLine(admin.TabularInline):
    model = Box
    extra = 1


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    inlines = [
        BoxInLine,
        ImageInLine
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'storage', 'image', 'get_preview']
    fields = ['storage', 'image', 'get_preview']
    readonly_fields = ('get_preview',)

    def get_preview(self, obj):
        return format_html(
            '<img src="{}" width="200" />',
            obj.image.url
        )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'box', 'start_rental_period',
                    'end_rental_period', 'is_payment', )
    readonly_fields = ['payment_id', 'stripe_payment_id']
