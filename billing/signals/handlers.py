from django.dispatch import receiver

from .signals import order_placed


@receiver(order_placed)
def placed_order(bh, **kwargs):
    from drfaddons.add_ons import send_message

    message = "You just placed an order at %s, Office Cafe. Order Number: %s | Total Amount %s. Greetings for eatings" \
              "^.^" % (bh.store.name, bh.order_no, bh.total)

    send_message(message, 'Order placed | Office Cafe', [bh.email], [bh.email])
    send_message(message, 'Order placed | Office Cafe', [bh.mobile], [bh.email])
