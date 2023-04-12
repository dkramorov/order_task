from django.contrib import admin
from base.admin import BaseAdmin
from . import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(BaseAdmin):
    inlines = [OrderItemInline]

