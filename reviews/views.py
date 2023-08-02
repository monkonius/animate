from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import requests
import json

from .models import User
from .forms import ReviewForm


def index(request):
    query = request.GET.get('q')
    if query:
        return render(request, 'reviews/search.html', {
            'query': query
        })

    return render(request, 'reviews/index.html')


def anime(request, anime_id):
    response = requests.get(f'https://api.jikan.moe/v4/anime/{anime_id}')
    data = json.loads(response.text)
    anime = data['data']

    if not request.user.is_anonymous:
        return render(request, 'reviews/anime.html', {
            'anime': anime,
            'form': ReviewForm()
        })

    return render(request, 'reviews/anime.html', {
        'anime': anime,
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged In!')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'Invalid username and/or password.')
            return render(request, 'reviews/login.html')
    else:
        return render(request, 'reviews/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out!')
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email =  request.POST['email']

        password = request.POST['password']
        confirm = request.POST['confirm']
        if password != confirm:
            messages.error(request, 'Passwords must match.')
            return render(request, 'reviews/register.html')
    
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            messages.error(request, 'Username already taken.')
            return render(request, 'reviews/register.html')
        login(request, user)
        messages.success(request, 'Account created!')
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'reviews/register.html')