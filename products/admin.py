from django.contrib import admin
from .models import Apply, Category, Product, Profile


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ApplyAdmin(admin.ModelAdmin):
    list_display = ['profile', 'accepted']
   

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price','available']
    list_filter = ['category', ]
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile)
admin.site.register(Apply,ApplyAdmin)