""" urls for the designers app. """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_designers, name='designers'),
    path('<int:designer_id>/', views.designer_detail, name='designer_detail'),
    path('add/', views.add_designer, name='add_designer'),
]
