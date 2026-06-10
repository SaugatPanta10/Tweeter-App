# tweets/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import RegistrationForm, TweetForm
from .models import Tweet

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Twitter, @{user.username}! Your account was created.")
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, @{user.username}!")
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def tweet_list(request):
    all_tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'tweets': all_tweets})

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, "Your tweet was posted successfully!")
            return redirect('/')
    else:
        form = TweetForm()
    return render(request, 'tweet_create.html', {'form': form})

@login_required
def tweet_edit(request, id):
    tweet = get_object_or_404(Tweet, id=id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            messages.success(request, "Tweet updated successfully!") 
            return redirect('/')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_edit.html', {'form': form, 'tweet': tweet})

@login_required
def tweet_delete(request, id):
    tweet = get_object_or_404(Tweet, id=id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        messages.success(request, "Your tweet has been permanently deleted.") 
        return redirect('/')
    return render(request, 'tweet_delete.html', {'tweet': tweet})