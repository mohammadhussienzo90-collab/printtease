from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'stock', 'available', 'created_at', 'image_preview')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('available', 'category', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('image_preview',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Product Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 10px;">', obj.image.url)
        return 'No Image'
    image_preview.short_description = 'Image Preview'