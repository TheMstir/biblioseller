from django.contrib import admin
from .models import Library, Category, LibImages


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['tittle']

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ["tittle", "description", "stock", "price", "sale", "in_pc_link"]


@admin.register(LibImages)
class LibraryImageAdmin(admin.ModelAdmin):
    list_display = ["name", "product", "image"]