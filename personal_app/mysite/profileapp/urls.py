from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('hobbies/', views.hobbies_view, name='hobbies'),
    path("contact/linkedin/", views.contact_linkedin, name="contact_linkedin"),
    path("contact/github/", views.contact_github, name="contact_github"),
    path("resume/", views.resume_view, name="resume"),
]
