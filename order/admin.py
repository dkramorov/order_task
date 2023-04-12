from django.contrib import admin
from base.admin import BaseAdmin
from . import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(BaseAdmin):
    inlines = [OrderItemInline]
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        #if change:
        #    obj.change_history(user_id=request.user.id, action='change', text='Изменение')


