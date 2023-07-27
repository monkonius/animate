from django.shortcuts import render
import requests
import json


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