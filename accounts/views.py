import os
import time

import qrcode
import qrcode.image.svg

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse

from accounts.forms import CustomUserCreationForm, ProfileForm, UserAuthenticationForm
from accounts.models import CustomUser
from storages.models import Rent


class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'my-rent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rents'] = Rent.objects.filter(tenant=self.request.user).order_by('box')
        return context

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])


class CustomLogoutView(LogoutView):
    next_page = 'index'


def signup_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # email = form.cleaned_data.get('email')
            # password = form.cleaned_data.get('password1')
            # account = authenticate(email=email, password=password)
            # login(request, account)
            login(request, user)
            messages.success(request, 'Успешная регистрация')
            return redirect(reverse('profile', args=[request.user.id]))
        else:
            messages.error(request, 'Ошибка регистрации. Форма заполнена неверно')
        form = CustomUserCreationForm()
    return render(request, 'index.html', {'signup_form': form})


def login_user(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Вы вошли в систему как {username}.')
                return redirect(reverse('profile', args=[request.user.id]))
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
        else:
            messages.error(request, 'Ошибка входа. Форма заполнена неверно')
    else:
        form = UserAuthenticationForm()
    return render(request, 'index.html', {'login_form': form})


def send_qrcode_to_email(request, rent_id):
    rent = Rent.objects.get(id=rent_id)

    generated_qrcode = qrcode.make(rent.payment_id)
    qrcode_filename = 'qr' + str(time.time()) + '.png'
    generated_qrcode.save(qrcode_filename)

    email = EmailMessage('QR-code', 'Your qr-code is in attachment', settings.EMAIL_HOST_USER, [request.user.email])
    email.attach_file(qrcode_filename)
    email.send()
    os.remove(qrcode_filename)

    return redirect(reverse('profile', args=[request.user.id]))
