from django.contrib import admin

from main.models import Payment, Product, Order, OrderItem, News

admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(News)
