from django.contrib import admin

from shopping_cart.models import Shopping_cart


@admin.register(Shopping_cart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    list_editable = (
        'user',
        'recipe'
    )
