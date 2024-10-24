from django.urls import path
from . import views  # Assuming views are in the same directory

urlpatterns = [
    path('', views.home, name='home'),  # Corrected home page route
    path('login/', views.login_user, name='login'),  
    path('logout/', views.logout_user, name='logout'), 
    path('register/', views.register, name='register'), 
    path('dashboard/', views.dashboard, name='dashboard'),

]
