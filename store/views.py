from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from .forms import ProfileForm, SignUpForm
from .models import Cart, Customer, OrderPlaced, Product


SHIPPING_AMOUNT = Decimal('70.00')
MOBILE_BRANDS = {'Vivo', 'Samsung', 'Iphone'}
LAPTOP_BRANDS = {'Hp', 'Dell', 'Apple'}


def _user_cart(user):
    return Cart.objects.filter(user=user).select_related('product')


def _cart_amount(cart_items):
    return sum((item.item_cost for item in cart_items), Decimal('0.00'))


def _cart_totals_response(cart_item, user):
    cart_items = _user_cart(user)
    amount = _cart_amount(cart_items)
    return JsonResponse({
        'quantity': cart_item.quantity,
        'amount': amount,
        'totalamount': amount + SHIPPING_AMOUNT,
    })


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        return render(request, 'store/home.html', {
            'topwears': topwears,
            'bottomwears': bottomwears,
            'mobiles': mobiles,
            'laptop': laptops,
        })


@login_required
def add_to_cart(request):
    product = get_object_or_404(Product, id=request.GET.get('prod_id'))
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save(update_fields=['quantity'])

    next_url = request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
    ):
        return redirect(next_url)
    return redirect('showcart')


@login_required
def address(request):
    addresses = Customer.objects.filter(user=request.user)
    return render(request, 'store/address.html', {'addres': addresses})


@login_required
def buy_now(request):
    return render(request, 'store/buy_now.html')


def bottom_wear(request):
    bottom = Product.objects.filter(category='BW')
    return render(request, 'store/bottom_wear.html', {'bottom': bottom})


@login_required
def checkout(request):
    addresses = Customer.objects.filter(user=request.user)
    items = _user_cart(request.user)
    amount = _cart_amount(items)
    total_amount = amount + SHIPPING_AMOUNT if amount else Decimal('0.00')
    return render(request, 'store/checkout.html', {
        'add': addresses,
        'total': total_amount,
        'items': items,
    })


def laptop(request, company=None):
    laptops = Product.objects.filter(category='L')
    if company in LAPTOP_BRANDS:
        laptops = laptops.filter(brand=company)
    return render(request, 'store/laptop.html', {'laptop': laptops})


@login_required
def minus_cart(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    cart_item = get_object_or_404(
        Cart,
        Q(product_id=request.GET.get('prod_id')) & Q(user=request.user),
    )
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save(update_fields=['quantity'])
    return _cart_totals_response(cart_item, request.user)


def mobile(request, data=None):
    mobiles = Product.objects.filter(category='M')
    if data in MOBILE_BRANDS:
        mobiles = mobiles.filter(brand=data)
    elif data == 'below':
        mobiles = mobiles.filter(discounted_price__lt=2500)
    elif data == 'above':
        mobiles = mobiles.filter(discounted_price__gt=2500)
    return render(request, 'store/mobile.html', {'mobiles': mobiles})


@login_required
def orders(request):
    order = OrderPlaced.objects.filter(
        user=request.user,
    ).select_related('product', 'customer')
    return render(request, 'store/orders.html', {'order': order})


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        already_cart = False
        if request.user.is_authenticated:
            already_cart = Cart.objects.filter(
                product=product,
                user=request.user,
            ).exists()
        return render(request, 'store/product_detail.html', {
            'product': product,
            'already': already_cart,
        })


@login_required
def profile(request):
    form = ProfileForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        customer = form.save(commit=False)
        customer.user = request.user
        customer.save()
        messages.success(request, 'Profile saved successfully.')
        form = ProfileForm()
    return render(request, 'store/profile.html', {'form': form})


@login_required
def plus_cart(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    cart_item = get_object_or_404(
        Cart,
        Q(product_id=request.GET.get('prod_id')) & Q(user=request.user),
    )
    cart_item.quantity += 1
    cart_item.save(update_fields=['quantity'])
    return _cart_totals_response(cart_item, request.user)


@login_required
def payment_done(request):
    if request.method != 'POST':
        return redirect('checkout')

    customer = get_object_or_404(
        Customer,
        id=request.POST.get('custid'),
        user=request.user,
    )
    cart_items = list(_user_cart(request.user))
    if not cart_items:
        return redirect('showcart')

    with transaction.atomic():
        OrderPlaced.objects.bulk_create([
            OrderPlaced(
                user=request.user,
                customer=customer,
                product=item.product,
                quantity=item.quantity,
            )
            for item in cart_items
        ])
        Cart.objects.filter(id__in=[item.id for item in cart_items]).delete()
    return redirect('orders')


@login_required
def remove_cart(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    cart_item = get_object_or_404(
        Cart,
        Q(product_id=request.GET.get('prod_id')) & Q(user=request.user),
    )
    cart_item.delete()

    cart_products = _user_cart(request.user)
    amount = _cart_amount(cart_products)
    return JsonResponse({
        'amount': amount,
        'totalamount': amount + SHIPPING_AMOUNT if amount else Decimal('0.00'),
        'empty_cart': not cart_products.exists(),
    })


@login_required
def show_cart(request):
    cart = _user_cart(request.user)
    amount = _cart_amount(cart)
    total_amount = amount + SHIPPING_AMOUNT if amount else Decimal('0.00')
    return render(request, 'store/cart.html', {
        'carts': cart,
        'total': total_amount,
        'ship': SHIPPING_AMOUNT,
        'amount': amount,
    })


def sign_up(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Account created successfully.')
        form = SignUpForm()
    return render(request, 'store/customer_registration.html', {'form': form})


def top_wear(request):
    top = Product.objects.filter(category='TW')
    return render(request, 'store/top_wear.html', {'top': top})
