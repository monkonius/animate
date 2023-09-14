from django.contrib import admin
from .models import User, Review, Like, Dislike

# Register your models here.
admin.site.register(User)
admin.site.register(Review)
admin.site.register(Like)
admin.site.register(Dislike)