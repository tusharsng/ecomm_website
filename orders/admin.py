from django.contrib import admin
from .models import Order,Payment
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter=('paid','total')
    search_fields = ['address', 'user']

class OrderitemAdmin(admin.ModelAdmin):
    list_display = ('order','price')
    list_filter=('price',)
   

admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, OrderitemAdmin)
