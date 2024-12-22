from django.contrib import admin
from .models import Product,Order
from django.contrib.auth.models import Group


admin.site.site_header="Stock Managment Dashboard"

class ProductAdmin(admin.ModelAdmin):
    list_display=('name','category','quantity','prixUnit')
    list_filter=['category']

class OderAdmin(admin.ModelAdmin):
    list_display=('product', 'orderQty', 'product_price', 'total_price', 'date','staff')   

    def product_price(self, obj): 
        return obj.product.prixUnit
    product_price.short_description = 'Product Price' 
    def total_price(self, obj): 
        return obj.total_price 
    total_price.short_description = 'Total Price'


# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OderAdmin)
#admin.site.unregister(Group)
