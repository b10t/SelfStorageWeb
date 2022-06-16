import stripe
from accounts.forms import CustomAuthenticationForm, CustomUserCreationForm
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse


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


def make_payment(request):
    """Производит платёж."""
    stripe.api_key = settings.STRIPE_API_KEY

    amount = 5000

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': f'Ваш заказ №',
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('successful_payment')),
        cancel_url=request.build_absolute_uri(reverse('cancelled_payment')),
    )

    return redirect(session.url, code=303)


def successful_payment(request):
    pass


def cancelled_payment(request):
    pass
