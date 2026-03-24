from django.contrib import admin
from django.utils.html import format_html
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "colored_name",
        "email",
        "subject",
        "is_read",
        "sent_at",
    )
    list_filter = (
        "is_read",
        "sent_at",
    )
    search_fields = (
        "name",
        "email",
        "subject",
        "message",
    )
    readonly_fields = (
        "sent_at",
        "ip_address",
    )
    list_editable = (
        "is_read",
    )
    ordering = ("-sent_at",)
    date_hierarchy = "sent_at"

    fieldsets = (
        ("Contact Info", {
            "fields": ("name", "email", "subject", "message")
        }),
        ("Tracking", {
            "fields": ("ip_address", "sent_at", "is_read")
        }),
    )

    def colored_name(self, obj):
        if not obj.is_read:
            return format_html(
                '<strong style="color:#dc3545;">{}</strong>',
                obj.name
            )
        return obj.name

    colored_name.short_description = "Name"
    colored_name.admin_order_field = "name"