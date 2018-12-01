from django.contrib import admin
from main.models import CustomUser, Post


@admin.register(CustomUser)
class ModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class ModelAdmin(admin.ModelAdmin):
    pass
