from django.urls import path
from . import views

urlpatterns = [
    path('', views.simple_view, name='simple_path'),
    path('reload/', views.reload_view, name='reload_path'),
]
