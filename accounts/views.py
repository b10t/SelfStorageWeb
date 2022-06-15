from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from accounts.forms import CustomUserCreationForm, ProfileForm, CustomAuthenticationForm


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'my-rent.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['subscribes'] = Subscribe.objects.filter(subscriber=self.request.user.id)
    #     return context

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])


class CustomLogoutView(LogoutView):
    next_page = 'index'


def signup_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успешная регистрация')
            return redirect('profile')
        else:
            messages.error(request, 'Ошибка регистрации. Форма заполнена неверно')
    else:
        form = CustomUserCreationForm()
    return render(request, 'index.html', {'signup_form': form})


def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Вы вошли в систему как {username}.')
                return redirect('index')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
        else:
            messages.error(request, 'Ошибка входа. Форма заполнена неверно')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'index.html', {'login_form': form})
