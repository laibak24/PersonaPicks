from django.conf.urls.static import static
from django.urls import path
from . import views  # Assuming views are in the same directory
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),  # Corrected home page route
    path('login/', views.login_user, name='login'),  
    path('logout/', views.logout_user, name='logout'), 
    path('register/', views.register, name='register'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('books/', views.books_view, name='books'),
    path('movies/', views.movies_view, name='movies'),
    path('songs/', views.songs_view, name='songs'),
    path('add_to_watchlist/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:movie_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),


] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
