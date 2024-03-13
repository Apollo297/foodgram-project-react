from django.contrib import admin

from subscriptions.models import Subscription

@admin.register(Subscription)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author'
    )
    list_editable = (
        'user',
        'author'
    )
    empty_value_display = '-пусто-'
