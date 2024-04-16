from django.contrib import admin
from .models import Order, Coupon

# Register your models here.

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to',
                    'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']


class OrderAdmin(admin.ModelAdmin):
    list_display =['academic_level', 'service_type', 'currency', 'price']


admin.site.register(Order, OrderAdmin)
