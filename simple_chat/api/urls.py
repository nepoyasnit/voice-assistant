from django.urls import path
from . import views
urlpatterns = [
    path('get_ai_response/', views.MessageAPI.as_view(), name='answer_question'),
]