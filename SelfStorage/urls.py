"""SelfStorage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from storages.views import (boxes, cancelled_payment, faq, index, make_payment,
                            my_rent, my_rent_empty, successful_payment)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('boxes/', boxes, name='boxes'),
    path('faq/', faq, name='faq'),
    path('my_rent_empty/', my_rent_empty, name='my_rent_empty'),
    path('my_rent/', my_rent, name='my_rent'),
    path('my_rent/', my_rent, name='my_rent'),
    path('make_payment/', make_payment, name='make_payment'),
    path('successful_payment/', successful_payment, name='successful_payment'),
    path('cancelled_payment/', cancelled_payment, name='cancelled_payment'),
    path('', index, name='index'),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
