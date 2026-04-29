from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from carts.models import CartItem
from products.models import Product
from .models import Order, OrderItem

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, 'Your cart is empty')
        return redirect('carts:cart')

    total = sum(item.total_price for item in cart_items)
    profile = request.user.profile if hasattr(request.user, 'profile') else None

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
        payment_method_id = request.POST.get('payment_method_id')

        # Create order
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
            total=total,
            payment_status='pending',
            stripe_payment_method_id=payment_method_id,
        )

        # Process payment with Stripe
        if payment_method_id:
            try:
                # Create payment intent
                intent = stripe.PaymentIntent.create(
                    amount=int(total * 100),  # Convert to cents
                    currency='usd',
                    payment_method=payment_method_id,
                    confirm=True,
                    return_url=request.build_absolute_uri('/orders/success/'),
                    metadata={'order_id': order.id}
                )

                order.stripe_payment_intent_id = intent.id
                order.payment_method = 'card'

                if intent.status == 'succeeded':
                    order.payment_status = 'paid'
                    order.status = 'processing'

                order.save()

            except stripe.error.CardError as e:
                messages.error(request, f'Payment failed: {e.error.message}')
                order.payment_status = 'failed'
                order.save()
                return render(request, 'orders/checkout.html', {
                    'cart_items': cart_items,
                    'total': total,
                    'profile': profile,
                    'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
                })
            except Exception as e:
                messages.error(request, f'Payment error: {str(e)}')
                order.payment_status = 'failed'
                order.save()

        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )

            # Update stock
            product = cart_item.product
            if product.stock >= cart_item.quantity:
                product.stock -= cart_item.quantity
                product.save()

        # Clear cart
        CartItem.objects.filter(user=request.user).delete()

        # Send confirmation email
        try:
            send_mail(
                f'Order Confirmation - PrintTease #{order.id}',
                f'Thank you for your order! Your order #{order.id} has been confirmed.\n\n'
                f'Total: ${order.total}\n'
                f'Payment Status: {order.get_payment_status_display()}\n\n'
                f'We will process and ship your order shortly.',
                'noreply@printtease.art',
                [email],
                fail_silently=True,
            )
        except:
            pass

        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('orders:order_detail', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'profile': profile,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    })


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if not request.user.is_superuser and order.user != request.user:
        from django.http import Http404
        raise Http404('Order not found')

    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


def payment_success(request):
    messages.success(request, 'Payment completed successfully!')
    return redirect('orders:order_history')


def payment_cancel(request):
    messages.error(request, 'Payment was cancelled. Please try again.')
    return redirect('carts:cart')