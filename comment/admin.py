from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Comment


class CommentInlineAdmin(GenericTabularInline):
    model = Comment
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
