from django.contrib.admin import ModelAdmin, register

from .models import CustomUser, Subscription


@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')


@register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    list_display = ('user', 'author')
