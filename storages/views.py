import stripe
from accounts.forms import CustomUserCreationForm, UserAuthenticationForm
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Count, Min, Q
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Box, City, Rent, Storage


def index(request):
    context = {
        'signup_form': CustomUserCreationForm,
        'login_form': UserAuthenticationForm,
    }

    return render(request, 'index.html', context)


def boxes(request):
    free_boxes_query = Count('boxes_in_storage', filter=Q(
        boxes_in_storage__is_available=True))
    storages = Storage.objects.prefetch_related('boxes_in_storage')\
        .select_related('city')\
        .annotate(free_boxes=free_boxes_query)\
        .annotate(boxes_count=Count('boxes_in_storage'))\
        .annotate(min_price=Min('boxes_in_storage__cost'))

    context = {"storages": storages}

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


def make_payment(request, payment_id):
    """Производит платёж."""
    stripe.api_key = settings.STRIPE_API_KEY

    try:
        rent = Rent.objects.get(payment_id=payment_id)
    except ValidationError:
        return HttpResponseNotFound('Неверный формат id платежа.')
    except Rent.DoesNotExist:
        return HttpResponseNotFound(f'Платёж {payment_id} не найден.')

    amount = rent.box.cost * 100

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
        success_url=request.build_absolute_uri(
            reverse('successful_payment', kwargs={'payment_id': payment_id})),
        cancel_url=request.build_absolute_uri(
            reverse('cancelled_payment', kwargs={'payment_id': payment_id})),
        client_reference_id=payment_id,
        customer_email=rent.tenant.email,
    )

    rent.stripe_payment_id = session.id
    rent.save()

    return redirect(session.url, code=303)


def successful_payment(request, payment_id):
    context = {}

    try:
        rent = Rent.objects.get(payment_id=payment_id)
    except ValidationError:
        return HttpResponseNotFound('Неверный формат id платежа.')
    except Rent.DoesNotExist:
        return HttpResponseNotFound(f'Платёж {payment_id} не найден.')

    rent.is_payment = True
    rent.save()

    return render(request, 'successful_payment.html', context)


def cancelled_payment(request, payment_id):
    context = {}

    return render(request, 'cancelled_payment.html', context)
