""" urls for the contact app. """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('manage/', views.manage_contacts, name='manage_contacts'),
    path(
        'toggle/<int:contact_message_id>/',
        views.toggle_responded, name='toggle_responded'),
]
