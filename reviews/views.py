from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import requests
import json

from .models import User

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

    return render(request, 'reviews/anime.html', {
        'anime': anime,
    })


def logout_view(request):
    logout(request)
    messages.success('Logged out!')
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