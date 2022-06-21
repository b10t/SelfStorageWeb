import stripe
from accounts.forms import CustomUserCreationForm, UserAuthenticationForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Count, Min, Q
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Box, Rent, Storage


def index(request):
    context = {
        'signup_form': CustomUserCreationForm,
        'login_form': UserAuthenticationForm,
    }

    return render(request, 'index.html', context)


def boxes(request):
    free_boxes_count_query = Count('boxes_in_storage', filter=Q(
        boxes_in_storage__is_available=True))

    storages = Storage.objects.prefetch_related('boxes_in_storage')\
        .select_related('city')\
        .annotate(free_boxes_count=free_boxes_count_query)\
        .annotate(boxes_count=Count('boxes_in_storage'))\
        .annotate(min_price=Min('boxes_in_storage__cost'))

    available_boxes = Box.objects.filter(is_available=True)

    context = {
        "storages": storages,
        "boxes": available_boxes,
    }

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


@login_required
def create_rent(request, box_id: int):
    """Создание заказа на аренду."""
    box = get_object_or_404(Box, pk=box_id)

    rent = Rent()
    rent.tenant = request.user
    rent.box = box
    rent.save()

    payment_url = request.build_absolute_uri(
        reverse('make_payment', kwargs={'payment_id': rent.payment_id}))

    return redirect(payment_url, code=303)


def make_payment(request, payment_id):
    """Производит платёж."""
    stripe.api_key = settings.STRIPE_API_KEY

    try:
        rent = Rent.objects.get(payment_id=payment_id)
    except ValidationError:
        return HttpResponseNotFound('Неверный формат id платежа.')
    except Rent.DoesNotExist:
        return HttpResponseNotFound(f'Платёж {payment_id} не найден.')

    if rent.is_payment:
        return HttpResponseNotFound(f'Платёж {payment_id} оплачен.')

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
