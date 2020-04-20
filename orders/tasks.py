from celery import task
from django.core.mail import send_mail
from .models import Order, OrderItem


# Task to send an email after successfully created order
@task
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
