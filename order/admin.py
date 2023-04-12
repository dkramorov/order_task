from django.contrib import admin
from . import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
