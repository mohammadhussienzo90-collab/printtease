from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import CartItem


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
        cart_items_session = request.session.get('cart_items', {})
        for product_id, quantity in cart_items_session.items():
            try:
                product = Product.objects.get(id=product_id, available=True)
                item = type('CartItem', (), {
                    'product': product,
                    'quantity': quantity,
                    'total_price': product.price * quantity
                })()
                cart_items.append(item)
            except Product.DoesNotExist:
                pass

    total = sum(item.total_price for item in cart_items)
    return render(request, 'carts/cart.html', {'cart_items': cart_items, 'total': total})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    else:
        cart_items = request.session.get('cart_items', {})
        if str(product_id) in cart_items:
            cart_items[str(product_id)] += quantity
        else:
            cart_items[str(product_id)] = quantity
        request.session['cart_items'] = cart_items

    messages.success(request, f'{product.name} added to cart')
    return redirect('carts:cart')


def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
        cart_item.delete()
    else:
        cart_items = request.session.get('cart_items', {})
        if str(product_id) in cart_items:
            del cart_items[str(product_id)]
            request.session['cart_items'] = cart_items
    return redirect('carts:cart')


def update_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        return remove_from_cart(request, product_id)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_items = request.session.get('cart_items', {})
        if str(product_id) in cart_items:
            cart_items[str(product_id)] = quantity
            request.session['cart_items'] = cart_items

    return redirect('carts:cart')