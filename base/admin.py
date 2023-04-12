from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author_create = request.user
        obj.author_update = request.user
        super().save_model(request, obj, form, change)
