from django.contrib import admin
from .models import Regular_pizza, Sicilian_pizza, Dinner_platters, Pasta, Salads, Subs, Toppings, OrderItem, Order
# Register your models here.

admin.site.register(Regular_pizza)
admin.site.register(Sicilian_pizza)
admin.site.register(Dinner_platters)
admin.site.register(Pasta)
admin.site.register(Salads)
admin.site.register(Subs)
admin.site.register(Toppings)
admin.site.register(OrderItem)
admin.site.register(Order)
