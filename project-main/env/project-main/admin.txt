from django.contrib import admin
from .models import Meal, Order, OrderMeal, Restaurant, DietPlan 

admin.site.register(Restaurant)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(OrderMeal)
admin.site.register(DietPlan)