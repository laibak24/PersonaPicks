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

    avatar_filename = f"{mbti_type}.jpg"
    avatar_path = os.path.join(settings.STATIC_URL, 'avatars', avatar_filename)

    # Get the user's watchlist with statuses
    watchlist = []
    watchlist_obj = Watchlist.objects.filter(watchlist_user=user).first()
    if watchlist_obj:
        watchlist = [{'movie': movie, 'status': watchlist_obj.status} for movie in watchlist_obj.movies.all()]

    # Get the user's readlist with statuses
    readlist = []
    readlist_obj = Readlist.objects.filter(readlist_user=user).first()
    if readlist_obj:
        readlist = [{'book': book, 'status': readlist_obj.status} for book in readlist_obj.books.all()]

    context = {
        'username': username,
        'mbti_type': mbti_type,
        'watchlist': watchlist,
        'readlist': readlist,
        'avatar_path': avatar_path,
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

@login_required
@require_POST
def add_to_readlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    readlist, created = Readlist.objects.get_or_create(readlist_user=request.user)

    if book not in readlist.books.all():
        readlist.books.add(book)
        message = f"'{book.title}' has been added to your readlist."

    else:
        message = f"'{book.title}' is already in your watchlist."

    # Fetch all movies again and pass the message back to the template
    books = Book.objects.all().order_by('title')
    return render(request, 'books.html', {'books': books, 'message': message})


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

@login_required
@require_POST
def remove_from_readlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    readlist = Readlist.objects.filter(readlist_user=request.user).first()

    if readlist and book in readlist.books.all():
        readlist.books.remove(book)
        messages.success(request, f"'{book.title}' has been removed from your readlist.")
    else:
        messages.warning(request, f"'{book.title}' is not in your readlist.")

    return redirect('dashboard')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback
from .forms import FeedbackForm

# View to give feedback
@login_required
def give_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.feedback_giver = request.user  # Set the user as the feedback giver
            feedback.save()
            return redirect('all_feedbacks')  # Redirect to feedback display page after saving
    else:
        form = FeedbackForm()
    return render(request, 'feedback/give_feedback.html', {'form': form})

def submit_feedback(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            feedback = Feedback(feedback_giver=request.user, message=message)
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
        else:
            messages.error(request, 'Please enter some feedback.')
    return redirect('dashboard')  # Redirect back to the dashboard

def top_picks(request):
    # Fetch all feedbacks
    feedbacks = Feedback.objects.all().order_by('-created_at')  # You can order by the creation date if needed
    return render(request, 'top_picks.html', {'feedbacks': feedbacks})
from django.shortcuts import redirect, get_object_or_404
from .models import Readlist, Book

@login_required
def update_readlist_status(request, book_id):
    if request.method == 'POST':
        # Get the selected status
        status = request.POST.get('status')
        # Find the readlist for the user and book
        readlist = Readlist.objects.filter(readlist_user=request.user).first()
        book = get_object_or_404(Book, book_id=book_id)
        
        if readlist and book in readlist.books.all():
            # Update the status
            readlist.status = status
            readlist.save()
    
    return redirect('dashboard')

@login_required
def update_watchlist_status(request, movie_id):
    if request.method == 'POST':
        # Get the selected status
        status = request.POST.get('status')
        # Find the watchlist for the user and movie
        watchlist = Watchlist.objects.filter(watchlist_user=request.user).first()
        movie = get_object_or_404(Movie, movie_id=movie_id)
        
        if watchlist and movie in watchlist.movies.all():
            # Update the status
            watchlist.status = status
            watchlist.save()
    
    return redirect('dashboard')
