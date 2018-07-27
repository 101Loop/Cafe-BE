from django.contrib import admin
from .models import Item, Tag, LunchPack, Store

# TODO: Customize admin site
# TODO: Show created_by, create_date, update_date in different section: Entry Details (For all models)
# TODO: Disable edit of create_date (For all models)
admin.site.register(Tag)

# TODO: Show table: name | category | price
# TODO: Filter by tag, category
# TODO: Search by name, tag, category
# TODO: Show tag & category in different section: Taggings
# TODO: Show gst, hsn, gst_inclusive in different section: Good & Service Tax Information
# TODO: Main section: name, price, desc, image
# TODO: Show price info: subtotal, total, gst
admin.site.register(Item)
admin.site.register(LunchPack)
admin.site.register(Store)
