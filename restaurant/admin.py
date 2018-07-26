from django.contrib import admin
from .models import Item, Tag, LunchPack, Store

admin.site.register(Tag)
admin.site.register(Item)
admin.site.register(LunchPack)
admin.site.register(Store)
