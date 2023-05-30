from django.contrib import admin

# Register your models here.
from cart.models import Cart, CartItem

admin.site.register(CartItem)
admin.site.register(Cart)