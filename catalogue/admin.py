from django.contrib import admin
from base.admin import BaseAdmin
from . import models


@admin.register(models.Product)
class ProductAdmin(BaseAdmin):
    pass
