from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm
from .models import Watchlist, Readlist

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
