from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), # for messanger page
    path('users/', include('django.contrib.auth.urls')),
    path('users/register/', views.Register.as_view(), name='register'), # view for registration
    path('representation/', TemplateView.as_view(template_name='chat/representation.html'),
         name='representation'), # welcome page
]
