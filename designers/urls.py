""" urls for the designers app. """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_designers, name='designers'),
]
