from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from shop.models import Product
from shop.models import Category


def OrderCreate(request):
    cart = Cart(request)
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    #  Processing cart to make order
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            return render(request, 'orders/order/created.html', {'order': order,
                                                                 'categories': categories,
                                                                 })

    form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form,
                                                        'products': products,
                                                        'categories': categories,
                                                        })
