from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Watchlist, Readlist

def home(request):
    return render(request, 'home.html')  # Ensure 'home.html' exists in the templates

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use 'get' for safety
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('home')
        else:
            messages.error(request, "Error logging in. Please check your credentials.")
            return redirect('login')  # Ensure 'login' URL is set correctly

    return render(request, 'login.html')  # Ensure 'login.html' exists in the templates

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')  # Correct message usage
    return redirect('home')



def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            messages.error(request, 'There was an error with your registration.')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def dashboard(request):
    watchlist = Watchlist.objects.filter(user=request.user).first()
    readlist = Readlist.objects.filter(user=request.user).first()

    context = {
        'user': request.user,
        'watchlist': watchlist,
        'readlist': readlist
    }
    return render(request, 'dashboard.html', context)
