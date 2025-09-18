from django.contrib import admin
from .models import Movie, Order, OrderItem
from .models import Movie, Order, OrderItem, Review

admin.site.register(Review)
admin.site.register(Movie)
admin.site.register(Order)
admin.site.register(OrderItem)
