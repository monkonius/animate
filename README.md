# Animate

*Animate* is an anime review web application built with Django, which uses the [Jikan REST API](https://docs.api.jikan.moe/) to access anime information from [MyAnimeList](https://myanimelist.net/). This is my final project for Harvard's Web Programming with Python and JavaScript course CS50W via their OpenCourseWare site.

#### Distinctiveness and Complexity:
This project is distinct from previous CS50W projects since it is a review web app that makes use of both an external and internal API, that is to say it accesses a third-party API (Jikan) and one written within the app (like and dislike functionality). For example, the third-party API is accessed to fetch top airing anime and specific anime information such as the number of episodes and its studio. It also has a sorting option for reviews listed in an anime's or user's page.

## Files:
The main logic of the app is found in `views.py`. The views are mapped to particular URLs found in the `urls.py` file. Note that certain URLs cannot be accessed by simply typing into the address bar as they require a POST method to access. For example, if a user attempts to like a post without appropriately clicking the like icon:
```
if request.method != 'POST':
        messages.error(request, 'That method is not allowed.')
        return HttpResponseRedirect(reverse('index'))
```

The `models.py` contains all the models needed for the web app, such as users, reviews, likes, and dislikes. The review form is created as a Form class from the Django review model since they already map closely to one another, which can be seen in `forms.py`.

`index.js` and `search.js` call upon the Jikan API in order to fetch and render the top airing anime and anime search results respectively. Their calls look like this:
```
const response = await fetch('https://api.jikan.moe/v4/top/anime?filter=airing');
const response = await fetch(`https://api.jikan.moe/v4/anime?q=${query.value}`);
```

`like.js`, on the other hand, makes use of the internal API whenever a user likes or dislikes a review. First, it sends the request:
```
fetch(`/like/${review.id}`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin'
    })
```
Then the logic in `views.py` will handle the request:
```
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
```

`review.js` and `dropdown.js` are simply for hiding and showing document elements on certain events. If a user is logged in, they can opt to write a review while they are on an anime's page, which will show the appropriate form. The dropdown menu can be accessed by clicking on the upper right portion of the document with the user icon and carat.

In addition to hiding and showing the review form, `review.js` also submits a form that sorts the reviews of an anime (if there are any) in `views.py`. An example where the reviews are ordered by likes:
```
reviews = (
    Review.objects.filter(anime_id=anime_id)
    .annotate(like_count=Count('likes'))
    .order_by('-like_count')
)
```

## Installation:
Clone the repository, create a virtual environment, and install the necessary packages from the requirements file.
```
git clone https://github.com/monkonius/animate
cd animate/
python3 -m venv .venv
pip3 install -r requirements.txt
```

## Usage:
Run the application while inside the activated virtual environment within the Animate repository.
```
. .venv/bin/activate
python3 manage.py runserver
```