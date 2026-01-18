from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get or create cart
    cart, created = Cart.objects.get_or_create(
        cart_id=_cart_id(request)
    )

    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        cart=cart,
    )

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()

    # ✅ MUST return response
    return redirect('cart')


def carts(request):
    return render(request, 'store/cart.html')
