""" urls for the designers app. """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_designers, name='designers'),
    path('<int:designer_id>/', views.designer_detail, name='designer_detail'),
    path('add/', views.add_designer, name='add_designer'),
    path('edit/<int:designer_id>/', views.edit_designer, name='edit_designer'),
    path(
        'delete/<int:designer_id>/',
        views.delete_designer, name='delete_designer'),
]
