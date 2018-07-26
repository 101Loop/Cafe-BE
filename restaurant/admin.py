from django.contrib import admin
from .models import Menu, Tag, Payment

admin.site.register(Tag)
admin.site.register(Menu)
admin.site.register(Payment)
