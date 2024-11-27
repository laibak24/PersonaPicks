from django.conf.urls.static import static
from django.urls import path
from . import views  # Assuming views are in the same directory
from django.conf import settings

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('about/', views.about, name='about'),

    # User Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<int:user_id>/', views.other_dashboard, name='other_dashboard'),

    # Books and Movies
    path('books/', views.books_view, name='books'),
    path('movies/', views.movies_view, name='movies'),
    path('add_to_watchlist/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('add_to_readlist/<int:book_id>/', views.add_to_readlist, name='add_to_readlist'),
    path('remove_from_watchlist/<int:movie_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('remove_from_readlist/<int:book_id>/', views.remove_from_readlist, name='remove_from_readlist'),
    path('give_feedback/', views.give_feedback, name='give_feedback'),
    path('top-picks/', views.top_picks, name='top_picks'),
    path('update_watchlist_status/<int:movie_id>/', views.update_watchlist_status, name='update_watchlist_status'),
    path('update_readlist_status/<int:book_id>/', views.update_readlist_status, name='update_readlist_status'),
    path('connect/', views.connect, name='connect'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('feedback/', views.give_feedback, name='give_feedback'),
    path('activity/', views.activity, name='activity'),

]
 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
