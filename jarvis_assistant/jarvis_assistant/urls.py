from django.contrib import admin
from django.urls import path
from authapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chat_response/', views.chat_response, name='chat_response'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
    path('reminders/', views.reminders, name='reminders'),
    path('add_reminder/', views.add_reminder, name='add_reminder'),
     path('delete_reminder/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    path('save_chat/', views.save_chat, name='save_chat'),
    path('chat_history/', views.chat_history, name='chat_history'),
    path('view_chat/<int:chat_id>/', views.view_chat, name='view_chat'),
    path('delete_chat/<int:chat_id>/', views.delete_chat, name='delete_chat'),
     path('feedback/', views.feedback_view, name='feedback'),
]

