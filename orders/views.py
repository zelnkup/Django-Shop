from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
# from .tasks import order_created
from shop.models import Product
from shop.models import Category
from django.core.mail import send_mail
from .models import Order


# django email backend
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {}.\nThis email confirms that you have successfully placed an order nr.  {}.\n For any information write to i.stebelskuy@gmail.com'.format(
        order.first_name, order.id)
    send_mail(subject,
              message,
              'pozdr.pl@gmail.com',
              [order.email])
    return send_mail


def OrderCreate(request):
    cart = Cart(request)
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    #  Processing cart to make order
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            # Django email backend
            order_created(order.id)

            return render(request, 'orders/order/created.html', {'order': order,
                                                                 'categories': categories,
                                                                 })

    form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form,
                                                        'products': products,
                                                        'categories': categories,
                                                        })
