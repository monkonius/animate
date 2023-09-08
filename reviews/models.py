from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    pass


class Review(models.Model):
    RECOMMENDATION = [
        ('RE', 'Recommended'),
        ('MF', 'Mixed Feelings'),
        ('NR', 'Not Recommended')
    ]

    id = models.BigAutoField(primary_key=True)
    anime_id = models.IntegerField()
    anime_title = models.CharField(max_length=256)
    content = models.TextField()
    recommendation = models.CharField(max_length=2, choices=RECOMMENDATION, default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review on anime no. {self.anime_id} by {self.author}'
    

class Like(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')


class Dislike(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='dislikes')