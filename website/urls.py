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

    # User Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<int:user_id>/', views.other_dashboard, name='other_dashboard'),

    # Books and Movies
    path('books/', views.books_view, name='books'),
    path('movies/', views.movies_view, name='movies'),

    # Watchlist and Readlist
    path('watchlist/add/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('readlist/add/<int:book_id>/', views.add_to_readlist, name='add_to_readlist'),
    path('watchlist/remove/<int:movie_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('readlist/remove/<int:book_id>/', views.remove_from_readlist, name='remove_from_readlist'),
    path('watchlist/update-status/<int:movie_id>/', views.update_watchlist_status, name='update_watchlist_status'),
    path('readlist/update-status/<int:book_id>/', views.update_readlist_status, name='update_readlist_status'),

    # Compatibility
    path('compatibility/<int:user_id>/', views.calculate_compatibility, name='calculate_compatibility'),

    # Feedback
    path('feedback/give/', views.give_feedback, name='give_feedback'),
    path('feedback/submit/', views.submit_feedback, name='submit_feedback'),

    # Connect and Profile
    path('connect/', views.connect, name='connect'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),

    # Top Picks
    path('top-picks/', views.top_picks, name='top_picks'),

    # About Page
    path('about/', views.about, name='about'),
]
 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
