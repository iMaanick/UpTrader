from django.contrib import admin
from menu.models import MenuItem


# Register your models here.
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'parent', 'menu_name')
    list_filter = ('title',)
    search_fields = ('title', 'url', 'menu_name')
    ordering = ('title',)


admin.site.register(MenuItem, MenuItemAdmin)
