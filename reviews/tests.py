from django.test import TestCase
from .models import Review, User


class ReviewTestCase(TestCase):
    def setUp(self):
        testuser = User.objects.create(
            username='testuser', email='testuser@email.com', password='password'
        )

        Review.objects.create(
            anime_id=1, content='test', recommendation='RE', author=testuser
        )
        Review.objects.create(
            anime_id=20, content='test', recommendation='MF', author=testuser
        )

    def test_review_count(self):
        user = User.objects.get(username='testuser')
        self.assertEqual(user.reviews.count(), 2)

    def test_review_content(self):
        review = Review.objects.get(anime_id=1)
        self.assertEqual(review.content, 'test')

    def test_review_recommendation(self):
        review = Review.objects.get(anime_id=20)
        self.assertEqual(review.recommendation, 'MF')
    
    def test_review_string_rep(self):
        review = Review.objects.get(anime_id=1)
        string = 'Review on anime no. 1 by testuser'
        self.assertEqual(str(review), string)