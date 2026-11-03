from django.contrib import admin
from .models import SiteSettings, MenuItem


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)