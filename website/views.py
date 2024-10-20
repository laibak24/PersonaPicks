from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

def home(request):
    return render(request, 'home.html')  # Make sure this matches the template name


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']  # Use username instead of email
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('home')
        else:
            messages.error(request, "Error logging in. Please check your credentials.")
            return redirect('login')  # Redirect back to the login page

    # Handle GET request (render the login page)
    return render(request, 'login.html')  # Make sure this matches the template name
        

def logout_user(request):
    pass 
