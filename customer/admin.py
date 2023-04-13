from django.contrib import admin
from base.admin import BaseAdmin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Organization)
class OrganizationAdmin(BaseAdmin):
    pass
