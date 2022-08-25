from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), # view for our messager
    path('users/', include('django.contrib.auth.urls')), # includes django's authentication urlmapping
    path('users/register/', views.Register.as_view(), name='register'), # view for registration
    path('representation/', views.TemplateView.as_view(template_name='chat/representation.html'),
         name='representation'), # view for representation of our project
]
