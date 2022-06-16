from django.shortcuts import render

from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm


def index(request):
    context = {
        'signup_form': CustomUserCreationForm,
        'login_form': CustomAuthenticationForm,
    }

    return render(request, 'index.html', context)


def boxes(request):
    context = {}

    return render(request, 'boxes.html', context)


def faq(request):
    context = {}

    return render(request, 'faq.html', context)


def my_rent_empty(request):
    context = {}

    return render(request, 'my-rent-empty.html', context)


def my_rent(request):
    context = {}

    return render(request, 'my-rent.html', context)
