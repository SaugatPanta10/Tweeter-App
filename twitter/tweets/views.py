from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, TweetForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Tweet

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

def tweet_list(request):
    all_tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'tweets': all_tweets})


def tweet_create(request):
    # This function handles creation of a new tweet

    if request.method == 'POST':
        # User submitted the tweet creation form

        form = TweetForm(request.POST, request.FILES)
        # Create form with:
        # - POST data (tweet text, etc.)
        # - FILES data (uploaded image if any)

        if form.is_valid():
            # Check if all submitted data is valid
            # according to the TweetForm rules

            tweet = form.save(commit=False)
            # Create Tweet object but do NOT save to database yet
            # We need to add the currently logged-in user first

            tweet.user = request.user
            # Assign the logged-in user as the owner/author
            # of this tweet

            tweet.save()
            # Save the completed Tweet object to the database

            return redirect('/')
            # Redirect user to homepage after successful tweet creation

    else:
        # If user is just opening the tweet creation page

        form = TweetForm()
        # Show an empty tweet creation form

    return render(request, 'tweet_create.html', {'form': form})
    # Render HTML page and send form to template

def tweet_edit(request, id):
    # This function handles editing an existing tweet

    tweet = get_object_or_404(Tweet, id=id, user=request.user)
    # Find the tweet with the given ID that belongs to the
    # currently logged-in user
    # If no such tweet exists, return a 404 error page
    # This prevents users from editing other users' tweets

    if request.method == 'POST':
        # User submitted the edit form

        form = TweetForm(request.POST, request.FILES, instance=tweet)
        # Create form with:
        # - updated text data from POST
        # - uploaded files from FILES
        # - existing tweet instance to update instead of creating a new one

        if form.is_valid():
            # Check if all submitted data is valid according
            # to the TweetForm validation rules

            form.save()
            # Save the updated tweet to the database

            return redirect('/')
            # Redirect user to homepage after successful update

    else:
        # User is opening the edit page (GET request)

        form = TweetForm(instance=tweet)
        # Create form pre-filled with the current tweet data
        # so the user can see and modify existing content

    return render(request, 'tweet_edit.html', {'form': form, 'tweet': tweet})
    # Render edit page and send:
    # - form (for displaying/editing fields)
    # - tweet object (if template needs tweet information)

# View for deleting a tweet
def tweet_delete(request, id):

    # Retrieve the tweet with the given ID that belongs to the currently logged-in user.
    # If no matching tweet is found, return a 404 error.
    tweet = get_object_or_404(Tweet, id=id, user=request.user)

    # Check if the request is a POST request.
    # This confirms that the user has submitted the delete confirmation form.
    if request.method == 'POST':

        # Permanently remove the tweet from the database.
        tweet.delete()

        # After deletion, redirect the user to the homepage.
        return redirect('/')

    # If the request is GET, display the confirmation page
    # and pass the tweet object to the template.
    return render(request, 'tweet_delete.html', {'tweet': tweet})