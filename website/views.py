from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, TestimonialForm
from .models import Watchlist, Readlist,Movie, Book, User, ActivityFeed, MBTIType, ReadlistItem, WatchlistItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages  # Import for messages
from django.urls import reverse
from .models import Testimonial



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

def about(request):
    if request.method == "POST":
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()  # Save the testimonial to the database
            return redirect('about')  # Redirect to the same page after submitting
    else:
        form = TestimonialForm()
    
    testimonials = Testimonial.objects.all().order_by('-created_at')  # Get all testimonials, latest first

    return render(request, 'about.html', {
        'form': form,
        'testimonials': testimonials
    })


# User Logout View
def logout_user(request):
    logout(request)
    return redirect('login')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Watchlist, Readlist, ActivityFeed, User
from .forms import EditBioForm  # Import the bio form
from django.conf import settings

import os


# Dashboard View
from django.db.models import Q
from .models import Watchlist, Readlist, ActivityFeed
from django.conf import settings

import os
@login_required
def dashboard(request):
    user = request.user

    # Fetching the avatar based on the MBTI type
    avatar_path = user.avatar.url if user.avatar else 'default_avatar.svg'

    # Retrieve watchlist and readlist items
    watchlist = WatchlistItem.objects.filter(user=user)
    readlist = ReadlistItem.objects.filter(user=user)

    # Retrieve activity feed
    activity_feed = ActivityFeed.objects.filter(
        Q(user=user) | Q(user__in=user.following.all())
    ).order_by('-created_at')[:10]

    # Calculate follower and following counts
    followers_count = user.followers.count()
    following_count = user.following.count()
# Handle bio form submission
    if request.method == 'POST':
        form = EditBioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect back to the dashboard after saving
    else:
        form = EditBioForm(instance=user)

    context = {
        'username': user.username,
        'bio': user.bio,
        'mbti_type': user.mbti_type.mbti_type if user.mbti_type else 'Not set',
        'avatar_path': avatar_path,
        'watchlist': watchlist,
        'readlist': readlist,
        'activity_feed': activity_feed,
        'followers_count': followers_count,  # Add follower count to context
        'following_count': following_count,  # Add following count to context
        'form': form,
    }

    return render(request, 'dashboard.html', context)
                  
@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, user_id=user_id)
    current_user = request.user

    if current_user == user_to_follow:
        return redirect('other_dashboard', user_id=user_id)  # Prevent self-following

    if user_to_follow in current_user.following.all():
        # Unfollow the user
        current_user.following.remove(user_to_follow)
        user_to_follow.followers.remove(current_user)  # Remove from followers as well
        ActivityFeed.objects.create(user=current_user, action=f"unfollowed {user_to_follow.username}")
    else:
        # Follow the user
        current_user.following.add(user_to_follow)
        user_to_follow.followers.add(current_user)  # Add to followers as well
        ActivityFeed.objects.create(user=current_user, action=f"followed {user_to_follow.username}")

    # Refresh both users to ensure counts are updated
    current_user.refresh_from_db()
    user_to_follow.refresh_from_db()

    # Recalculate follower and following counts after the update
    followers_count = user_to_follow.followers.count()
    following_count = current_user.following.count()

    # Redirect to the user's profile with the updated counts
    return redirect('other_dashboard', user_id=user_id)

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


@login_required
@require_POST
def add_to_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    # Check if the movie is already in the user's watchlist
    if not WatchlistItem.objects.filter(user=request.user, movie=movie).exists():
        WatchlistItem.objects.create(user=request.user, movie=movie, status='not_started')
        message = f"'{movie.title}' has been added to your watchlist."
        # Log the action of adding a movie
        ActivityFeed.objects.create(user=request.user, action=f"added '{movie.title}' to their watchlist.")
    else:
        message = f"'{movie.title}' is already in your watchlist."

    return redirect('dashboard')

@login_required
@require_POST
def add_to_readlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    # Check if the book is already in the user's readlist
    if not ReadlistItem.objects.filter(user=request.user, book=book).exists():
        ReadlistItem.objects.create(user=request.user, book=book, status='not_started')
        message = f"'{book.title}' has been added to your readlist."
        # Log the action of adding a book
        ActivityFeed.objects.create(user=request.user, action=f"added '{book.title}' to their readlist.")
    else:
        message = f"'{book.title}' is already in your readlist."

    return redirect('dashboard')

@login_required
@require_POST
def remove_from_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    # Find and delete the WatchlistItem
    watchlist_item = WatchlistItem.objects.filter(user=request.user, movie=movie).first()
    if watchlist_item:
        watchlist_item.delete()
        messages.success(request, f"'{movie.title}' has been removed from your watchlist.")
        # Log the removal action
        ActivityFeed.objects.create(user=request.user, action=f"removed '{movie.title}' from their watchlist.")
    else:
        messages.warning(request, f"'{movie.title}' is not in your watchlist.")

    return redirect('dashboard')

@login_required
@require_POST
def remove_from_readlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    # Find and delete the ReadlistItem
    readlist_item = ReadlistItem.objects.filter(user=request.user, book=book).first()
    if readlist_item:
        readlist_item.delete()
        messages.success(request, f"'{book.title}' has been removed from your readlist.")
        # Log the removal action
        ActivityFeed.objects.create(user=request.user, action=f"removed '{book.title}' from their readlist.")
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


@login_required
def update_watchlist_status(request, movie_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        watchlist_item = get_object_or_404(WatchlistItem, user=request.user, movie__movie_id=movie_id)
        watchlist_item.status = status
        watchlist_item.save()
    return redirect('dashboard')

@login_required
def update_readlist_status(request, book_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        readlist_item = get_object_or_404(ReadlistItem, user=request.user, book__book_id=book_id)
        readlist_item.status = status
        readlist_item.save()
    return redirect('dashboard')


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CompatibilityScore, User, MBTIType
from django.db.models import Q
def compare_mbti_types(user_1, user_2):
    """
    Calculate compatibility score between two users based on their MBTI types.

    Args:
        user_1 (User): First user instance.
        user_2 (User): Second user instance.

    Returns:
        float: Compatibility score (0 to 100).
    """
    if not user_1.mbti_type or not user_2.mbti_type:
        return 0.0  # Return 0 if either user doesn't have an MBTI type assigned.

    mbti_type_1 = user_1.mbti_type.mbti_type
    mbti_type_2 = user_2.mbti_type.mbti_type

    if len(mbti_type_1) != 4 or len(mbti_type_2) != 4:
        return 0.0  # Return 0 if MBTI types are not valid 4-character strings.

    # Compatibility scoring
    compatibility_score = 0
    dimensions = ['I/E', 'S/N', 'T/F', 'J/P']

    for i in range(4):  # Compare each character in the MBTI type
        if mbti_type_1[i] == mbti_type_2[i]:
            compatibility_score += 1  # Fully compatible on this dimension

    # Normalize to 0-100 scale
    return compatibility_score * 25  # 4 dimensions, each worth 25 points

from .models import CompatibilityScore, User

@login_required
def calculate_compatibility(request, user_id):
    user = request.user  # Current logged-in user
    compared_user = get_object_or_404(User, id=user_id)  # User to compare with

    # Get the MBTI types of both users
    user_mbti = getattr(user.mbti_type, 'mbti_type', None)
    compared_user_mbti = getattr(compared_user.mbti_type, 'mbti_type', None)

    if user_mbti and compared_user_mbti:
        # Calculate compatibility score
        score = compare_mbti_types(user_mbti, compared_user_mbti)

        # Update or create the compatibility score (user -> compared_user)
        CompatibilityScore.objects.update_or_create(
            user=user,
            compared_user=compared_user,
            defaults={'score': score}
        )
        # Update or create the reverse compatibility score (compared_user -> user)
        CompatibilityScore.objects.update_or_create(
            user=compared_user,
            compared_user=user,
            defaults={'score': score}
        )

        return redirect('other_dashboard', user_id=compared_user.id)

    # Redirect with an error message if MBTI types are missing
    messages.error(request, "MBTI types are missing for one or both users.")
    return redirect('other_dashboard', user_id=compared_user.id)

def about(request):
    feedback_form = FeedbackForm()
    feedbacks = Feedback.objects.all()  # Or any logic to fetch feedbacks
    context = {
        'feedback_form': feedback_form,
        'feedbacks': feedbacks,
    }
    return render(request, 'about.html', context)

@login_required
def top_picks(request):
    user_mbti_type = request.user.mbti_type  # Assuming the User model has the mbti_type attribute
    
    # Get movies that match the user's MBTI preferences
    movies = Movie.objects.filter(
        first_preference=user_mbti_type
    ) | Movie.objects.filter(
        second_preference=user_mbti_type
    ) | Movie.objects.filter(
        third_preference=user_mbti_type
    )
    
    # Get books that match the user's MBTI preferences
    books = Book.objects.filter(
        first_preference=user_mbti_type
    ) | Book.objects.filter(
        second_preference=user_mbti_type
    ) | Book.objects.filter(
        third_preference=user_mbti_type
    )

    return render(request, 'top_picks.html', {'movies': movies, 'books': books})
from django.db.models import Q

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import User, MBTIType, Movie, Book

@login_required
def connect(request):
    # Get the current logged-in user
    current_user = request.user
    
    # If there's a search query, filter users by MBTI type
    mbti_filter = request.GET.get('mbti_type', None)
    
    # Fetch all users except the current one
    users = User.objects.exclude(user_id=current_user.user_id)  # Use `user_id` as primary key

    # Filter users by MBTI type if a search is provided
    if mbti_filter:
        users = users.filter(mbti_type__mbti_type=mbti_filter)
    
    # Get all MBTI types for the search filter dropdown
    mbti_types = MBTIType.objects.all()

    context = {
        'users': users,
        'mbti_types': mbti_types,
        'current_user': current_user,
    }
    return render(request, 'connect.html', context)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, WatchlistItem, ReadlistItem, CompatibilityScore

@login_required
def other_dashboard(request, user_id):
    selected_user = get_object_or_404(User, user_id=user_id)

    # Calculate the follower and following counts
    followers_count = selected_user.followers.count()
    following_count = selected_user.following.count()

    # Fetching watchlist and readlist items
    watchlist_movies = WatchlistItem.objects.filter(user=selected_user)
    readlist_books = ReadlistItem.objects.filter(user=selected_user)

    # Calculate compatibility score
    try:
        compatibility_score = CompatibilityScore.objects.get(user=request.user, compared_user=selected_user).score
    except CompatibilityScore.DoesNotExist:
        compatibility_score = 0  # Fallback value if no score exists

    # Pass context to template
    context = {
        'selected_user': selected_user,
        'watchlist_movies': watchlist_movies,
        'readlist_books': readlist_books,
        'compatibility_score': compatibility_score,
        'followers_count': followers_count,
        'following_count': following_count,
    }

    return render(request, 'other_dashboard.html', context)
