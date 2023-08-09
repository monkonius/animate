# Animate

*Animate* is an anime review web application built with Django, which uses the [Jikan REST API](https://docs.api.jikan.moe/) to access anime information from [MyAnimeList](https://myanimelist.net/). This is my final project for Harvard's Web Programming with Python and JavaScript course CS50W via their OpenCourseWare site.

#### Distinctiveness and Complexity:
This project is distinct from previous projects since it makes use of both an external and internal API, that is to say it accesses a third-party API (Jikan) and one written within the app (like functionality).

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
python3 manage.py runserver
```