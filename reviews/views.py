from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json

from .models import User, Review, Like, Dislike
from .forms import ReviewForm


def index(request):
    query = request.GET.get('q')
    if query:
        return render(request, 'reviews/search.html', {
            'query': query
        })

    return render(request, 'reviews/index.html')


def random(request):
    response = requests.get('https://api.jikan.moe/v4/random/anime')
    data = json.loads(response.text)
    anime = data['data']

    messages.success(request, 'Random anime chosen!')
    return HttpResponseRedirect(reverse('anime', kwargs={'anime_id': anime['mal_id']}))


def anime(request, anime_id):
    response = requests.get(f'https://api.jikan.moe/v4/anime/{anime_id}')
    data = json.loads(response.text)
    anime = data['data']

    sorting = request.GET.get('sort-by')
    selected = {
        'latest': False,
        'oldest': False,
        'likes': False,
        'dislikes': False
    }

    if sorting == 'oldest':
        reviews = Review.objects.filter(anime_id=anime_id).order_by('time')
        selected['oldest'] = True
    elif sorting == 'likes':
        reviews = (
            Review.objects.filter(anime_id=anime_id)
            .annotate(like_count=Count('likes'))
            .order_by('-like_count')
        )
        selected['likes'] = True
    elif sorting == 'dislikes':
        reviews = (
            Review.objects.filter(anime_id=anime_id)
            .annotate(dislike_count=Count('dislikes'))
            .order_by('-dislike_count')
        )
        selected['dislikes'] = True
    else:
        reviews = Review.objects.filter(anime_id=anime_id).order_by('-time')
        selected['latest'] = True

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            anime_id = request.POST.get('anime_id')
            anime_title = request.POST.get('anime_title')
            content = form.cleaned_data['content']
            recommendation = form.cleaned_data['recommendation']
            author = request.user

            new_review = Review(
                anime_id=int(anime_id), anime_title=anime_title,
                content=content, recommendation=recommendation, author=author
            )
            new_review.save()

            messages.success(request, 'Review posted!')
            return HttpResponseRedirect(reverse('anime', kwargs={'anime_id': anime_id}))

    if not request.user.is_anonymous:
        user = User.objects.get(id=request.user.id)
        liked_reviews = list(map(lambda x: x.review, user.likes.all()))
        disliked_reviews = list(map(lambda x: x.review, user.dislikes.all()))

        return render(request, 'reviews/anime.html', {
            'anime': anime,
            'reviews': reviews,
            'liked_reviews': liked_reviews,
            'disliked_reviews': disliked_reviews,
            'form': ReviewForm(),
            'selected': selected
        })

    return render(request, 'reviews/anime.html', {
        'anime': anime,
        'reviews': reviews,
        'selected': selected
    })


@login_required
def like(request, review_id):
    if request.method != 'POST':
        messages.error(request, 'That method is not allowed.')
        return HttpResponseRedirect(reverse('index'))
    
    user = User.objects.get(id=request.user.id)
    review = Review.objects.get(id=review_id)

    like, created = Like.objects.get_or_create(user=user, review=review)
    dislike = Dislike.objects.filter(user=user, review=review)
    dislike_exists = dislike.exists()
    if not created:
        like.delete()
    else:
        review.likes.add(like)
        if dislike_exists:
            dislike.delete()

    return JsonResponse({'created': created, 'dislike_exists': dislike_exists}, status=201)


@login_required
def dislike(request, review_id):
    if request.method != 'POST':
        messages.error(request, 'That method is not allowed.')
        return HttpResponseRedirect(reverse('index'))
    
    user = User.objects.get(id=request.user.id)
    review = Review.objects.get(id=review_id)

    dislike, created = Dislike.objects.get_or_create(user=user, review=review)
    like = Like.objects.filter(user=user, review=review)
    like_exists = like.exists()
    if not created:
        dislike.delete()
    else:
        review.dislikes.add(dislike)
        if like_exists:
            like.delete()

    return JsonResponse({'created': created, 'like_exists': like_exists}, status=201)


def profile(request, username):
    profile_user = User.objects.get(username=username)

    sorting = request.GET.get('sort-by')
    selected = {
        'latest': False,
        'oldest': False,
        'likes': False,
        'dislikes': False
    }

    if sorting == 'oldest':
        reviews = Review.objects.filter(author=profile_user.id).order_by('time')
        selected['oldest'] = True
    elif sorting == 'likes':
        reviews = (
            Review.objects.filter(author=profile_user.id)
            .annotate(like_count=Count('likes'))
            .order_by('-like_count')
        )
        selected['likes'] = True
    elif sorting == 'dislikes':
        reviews = (
            Review.objects.filter(author=profile_user.id)
            .annotate(dislike_count=Count('dislikes'))
            .order_by('-dislike_count')
        )
        selected['dislikes'] = True
    else:
        reviews = Review.objects.filter(author=profile_user.id).order_by('-time')
        selected['latest'] = True

    if not request.user.is_anonymous:
        user = User.objects.get(id=request.user.id)
        liked_reviews = list(map(lambda x: x.review, user.likes.all()))
        disliked_reviews = list(map(lambda x: x.review, user.dislikes.all()))

        return render(request, 'reviews/profile.html', {
            'profile_username': profile_user.username,
            'reviews': reviews,
            'liked_reviews': liked_reviews,
            'disliked_reviews': disliked_reviews,
            'selected': selected
        })

    return render(request, 'reviews/profile.html', {
        'profile_username': profile_user.username,
        'reviews': reviews,
        'selected': selected
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