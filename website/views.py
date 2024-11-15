from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm
from .models import Watchlist, Readlist,Movie,Song, Book
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages  # Import for messages


def home(request):
    return render(request, 'home.html')




@login_required
@require_POST
def remove_from_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    watchlist = Watchlist.objects.filter(watchlist_user=request.user).first()

    if watchlist and movie in watchlist.movies.all():
        watchlist.movies.remove(movie)
        messages.success(request, f"'{movie.title}' has been removed from your watchlist.")
    else:
        messages.warning(request, f"'{movie.title}' is not in your watchlist.")

    return redirect('dashboard')

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # This retrieves the email
            password = request.POST.get('password')  # Get the password directly from POST data
            
            # Use the username parameter instead of email in authenticate
            user = authenticate(request, username=email, password=password)  # Change here
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})

# User Logout View
def logout_user(request):
    logout(request)
    return redirect('login')

# Dashboard View
from django.conf import settings
import os

# Dashboard View
@login_required
def dashboard(request):
    user = request.user
    username = user.username
    mbti_type = user.mbti_type.mbti_type if user.mbti_type else 'Not set'

    # Construct the path for the avatar
    avatar_filename = f"{mbti_type}.jpg"  # Assuming the files are named as MBTI type (e.g., 'INFP.jpeg')
    avatar_path = os.path.join(settings.STATIC_URL, 'avatars', avatar_filename)

    # Get the user's watchlist and readlist
    watchlist = Watchlist.objects.filter(watchlist_user=user).first().movies.all() if Watchlist.objects.filter(watchlist_user=user).exists() else []
    readlist = Readlist.objects.filter(readlist_user=user).first().books.all() if Readlist.objects.filter(readlist_user=user).exists() else []

    context = {
        'username': username,
        'mbti_type': mbti_type,
        'watchlist': watchlist,
        'readlist': readlist,
        'avatar_path': avatar_path,  # Add avatar path to context
    }

    return render(request, 'dashboard.html', context)

# Books View
def books_view(request):
    # Fetch all books along with MBTI preferences
    books = Book.objects.all().order_by('title')  # Order alphabetically by title or customize ordering as needed
    
    # Pass books to the template
    context = {
        'books': books,
    }
    return render(request, 'books.html', context)

def movies_view(request):
    # Fetch all movies along with MBTI preferences
    movies = Movie.objects.all().order_by('title')  # Order alphabetically by title or customize ordering as needed
    
    # Pass movies to the template
    context = {
        'movies': movies,
    }
    return render(request, 'movies.html', context)

# Songs View
def songs_view(request):
    # Fetch all songs along with their MBTI preferences
    songs = Song.objects.all().order_by('title')  # Order alphabetically by song title

    # Pass songs to the template
    context = {
        'songs': songs,
    }
    return render(request, 'songs.html', context)



@login_required
@require_POST
def add_to_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    watchlist, created = Watchlist.objects.get_or_create(watchlist_user=request.user)

    if movie not in watchlist.movies.all():
        watchlist.movies.add(movie)
        message = f"'{movie.title}' has been added to your watchlist."
    else:
        message = f"'{movie.title}' is already in your watchlist."

    # Fetch all movies again and pass the message back to the template
    movies = Movie.objects.all().order_by('title')
    return render(request, 'movies.html', {'movies': movies, 'message': message})
