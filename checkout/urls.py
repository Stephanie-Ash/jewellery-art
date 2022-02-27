""" urls for the checkout app. """
from django.urls import path
from . import views
from .webhooks import webhook


urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('login_or_guest/', views.login_or_guest, name='login_or_guest'),
    path(
        'checkout_success/<order_number>/', views.checkout_success,
        name='checkout_success'),
    path(
        'cache_checkout_data/', views.cache_checkout_data,
        name='cache_checkout_data'),
    path('update_inventory/', views.update_inventory, name='update_inventory'),
    path('wh/', webhook, name='webhook'),
]
