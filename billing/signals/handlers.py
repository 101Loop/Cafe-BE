from django.dispatch import receiver

from .signals import order_placed


@receiver(order_placed)
def placed_order(bh, **kwargs):
    from drfaddons.add_ons import send_message

    if bh.total < 9:
        message = """You just placed an order at %s, Office Cafe.
Order Number: %s
Total: %s :PENDING
Pay at Store only.
Greetings for eatings ^.^""" % (bh.store.name, bh.id, round(bh.total, 2))
    else:
        message = """You just placed an order at %s, Office Cafe.
Order Number: %s
Total Amount %s :PAID
Greetings for eatings ^.^""" % (bh.store.name, bh.id, round(bh.total, 2))

    items = ''
    for itm in bh.billitem_set.all():
        items += '%s - %s' % (itm.item.name, itm.quantity)

    if bh.paid:
        paid = 'Yes'
    else:
        paid = 'No'

    store_message = """%s just placed an order
Paid: %s
Amount: %s
Mobile: %s
Item: %s""" % (bh.name, paid, round(bh.total, 2), bh.mobile, items)

    send_message(message, 'Order placed | Office Cafe', [bh.email], [bh.email])
    send_message(message, 'Order placed | Office Cafe', [bh.mobile], [bh.email])

    send_message(store_message, 'Order placed | Office Cafe', ['admin@officecafe.in'], ['admin@officecafe.in'])
    send_message(store_message, 'Order placed | Office Cafe', [bh.store.mobile], ['admin@officecafe.in'])
