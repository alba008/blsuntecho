# BLSUNTECH_INQUIRY_ADMIN_V2

from django.contrib import admin
from django.utils.html import format_html
from .models import BusinessInquiry


@admin.register(BusinessInquiry)
class BusinessInquiryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "company",
        "service",
        "status_indicator",
        "created_at",
    )

    list_filter = (
        "status",
        "service",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "company",
        "message",
    )

    readonly_fields = (
        "name",
        "email",
        "company",
        "service",
        "message",
        "created_at",
    )

    fields = (
        "status",
        "name",
        "email",
        "company",
        "service",
        "message",
        "created_at",
    )

    list_per_page = 25
    ordering = ("-created_at",)

    actions = (
        "mark_reviewing",
        "mark_contacted",
        "mark_closed",
    )

    @admin.display(description="Status", ordering="status")
    def status_indicator(self, obj):
        colors = {
            "new": "#222222",
            "reviewing": "#666666",
            "contacted": "#777777",
            "closed": "#999999",
        }

        color = colors.get(obj.status, "#222222")

        return format_html(
            '<span style="color:{};font-weight:700">{}</span>',
            color,
            obj.get_status_display(),
        )

    @admin.action(description="Mark selected as Reviewing")
    def mark_reviewing(self, request, queryset):
        count = queryset.update(status="reviewing")
        self.message_user(request, f"{count} inquiries updated.")

    @admin.action(description="Mark selected as Contacted")
    def mark_contacted(self, request, queryset):
        count = queryset.update(status="contacted")
        self.message_user(request, f"{count} inquiries updated.")

    @admin.action(description="Mark selected as Closed")
    def mark_closed(self, request, queryset):
        count = queryset.update(status="closed")
        self.message_user(request, f"{count} inquiries updated.")


admin.site.site_header = "BlsunTech Dynamics"
admin.site.site_title = "BlsunTech Administration"
admin.site.index_title = "Business Management"
