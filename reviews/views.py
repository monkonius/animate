from django.shortcuts import render


def index(request):
    query = request.GET.get('q')
    if query:
        return render(request, "reviews/search.html", {
            "query": query
        })

    return render(request, "reviews/index.html")