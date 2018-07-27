from django.contrib import admin
from .models import Item, Tag, LunchPack, Store, HasItem


class MyModelAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        """
        Makes created_by & create_date readonly when editing.
        """
        if not obj:
            return ()
        return 'created_by', 'create_date'

# TODO: Customize admin site
# TODO: Show created_by, create_date, update_date in different section: Entry Details (For all models)

admin.site.register(Tag)

# TODO: Show table: name | category | price
# TODO: Filter by tag, category
# TODO: Search by name, tag, category
# TODO: Show tag & category in different section: Taggings
# TODO: Show gst, hsn, gst_inclusive in different section: Good & Service Tax Information
# TODO: Main section: name, price, desc, image
# TODO: Show price info: subtotal, total, gst
admin.site.register(Item, MyModelAdmin)
admin.site.register(LunchPack, MyModelAdmin)
admin.site.register(Store, MyModelAdmin)
admin.site.register(HasItem, MyModelAdmin)
