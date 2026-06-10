from django.shortcuts import render, redirect
from .forms import RegistrationForm, TweetForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(request):
    return render(request, 'base.html')

def register_view(request): 
    # This function handles user registration page

    if request.method == 'POST':
        # User submitted the registration form

        form = RegistrationForm(request.POST)
        # Create form with data sent by user (username, password, etc.)

        if form.is_valid():
            # Check if all data is correct:
            # - username not empty
            # - username not already taken
            # - passwords match
            # - password meets rules

            user = form.save()
            # Save the new user into the database

            login(request, user)
            # Log the user in immediately after registration

            return redirect('/')
            # Send user to homepage after successful signup

    else:
        # If user is just opening the page (GET request)
        form = RegistrationForm()
        # Show empty registration form

    return render(request, 'register.html', {'form': form})
    # Render HTML page and send form to template

def login_view(request):
    # This function handles user login

    if request.method == 'POST':
        # User submitted login form

        form = AuthenticationForm(request, request.POST)
        # Create authentication form with:
        # - request (needed for session handling)
        # - POST data (username + password)

        if form.is_valid():
            # Check if credentials are correct:
            # - user exists in database
            # - password matches hashed password

            user = form.get_user()
            # Get the authenticated user object

            login(request, user)
            # Log the user in (start session)

            return redirect('/')
            # Redirect to homepage after login

    else:
        # If user is just opening login page
        form = AuthenticationForm()
        # Show empty login form

    return render(request, 'login.html', {'form': form})
    # Render login page with form

def logout_view(request):
    # This function logs the user out

    if request.method == 'POST' or request.method == 'GET':
        # Works for both POST and GET requests

        logout(request)
        # Remove user session (user becomes anonymous)

        return redirect('/')
        # Redirect to homepage after logout

def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('/')
    else:
        form = TweetForm()
    return render(request, 'tweet_create.html', {'form': form})