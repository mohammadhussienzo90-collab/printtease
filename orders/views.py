from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from carts.models import CartItem
from products.models import Product
from .models import Order, OrderItem


@login_required
def checkout(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country', 'USA')

        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items:
            messages.error(request, 'Your cart is empty')
            return redirect('carts:cart')

        total = sum(item.total_price for item in cart_items)

        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            total=total
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )

            product = cart_item.product
            if product.stock >= cart_item.quantity:
                product.stock -= cart_item.quantity
                product.save()

        CartItem.objects.filter(user=request.user).delete()
        messages.success(request, f'Order {order.id} placed successfully!')
        return redirect('orders:order_detail', order_id=order.id)

    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    profile = request.user.profile

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'profile': profile
    })


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)

    if not request.user.is_superuser and order.user != request.user:
        from django.http import Http404
        raise Http404('Order not found')

    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})