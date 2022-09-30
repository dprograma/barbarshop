from django.urls import path

# local modules
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('book-appointment/', views.bookAppointment, name='book-appointment'),
]