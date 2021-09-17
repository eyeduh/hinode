
from django.contrib import admin

# Register your models here.
from .models import Node, NodeComment, NodeLike


class NodeLikeAdmin(admin.TabularInline):
    model = NodeLike


class NodeCommentAdmin(admin.TabularInline):
    model = NodeComment


class NodeAdmin(admin.ModelAdmin):
    inlines = [NodeLikeAdmin, NodeCommentAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']

    class Meta:
        model = Node


admin.site.register(Node, NodeAdmin)
