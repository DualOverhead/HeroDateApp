from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.homeView,name='home'),
    path('', views.introView,name='intro'),
    path('message/', views.sendMessage,name='message'),
    path('messagesent/', views.messageSent, name='messagesent'),
]


