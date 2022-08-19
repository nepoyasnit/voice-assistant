from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('users/', include('django.contrib.auth.urls')),
    path('users/register/', views.Register.as_view(), name='register'),
]
