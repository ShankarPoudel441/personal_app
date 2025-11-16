from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('hobbies/', views.hobbies_view, name='hobbies'),
]
