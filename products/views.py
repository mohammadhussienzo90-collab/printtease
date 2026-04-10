from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from carts.models import CartItem
from carts.views import _cart_id


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'products/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = None
    in_cart = False

    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.filter(product=product).first()
            if cart_item:
                in_cart = True
        except CartItem.DoesNotExist:
            pass
    else:
        cart_items = request.session.get('cart_items', {})
        in_cart = str(product.id) in cart_items

    return render(request, 'products/product/detail.html', {
        'product': product,
        'in_cart': in_cart,
    })