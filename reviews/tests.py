from django.test import Client, TestCase
from .models import Review, User


class ReviewTestCase(TestCase):
    def setUp(self):
        testuser = User.objects.create_user('testuser', 'testuser@email.com', 'password')
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


class PageTests(TestCase):
    def setUp(self):
        testuser = User.objects.create_user('testuser', 'testuser@email.com', 'password')
        Review.objects.create(
            anime_id=1, content='test', recommendation='RE', author=testuser
        )
        Review.objects.create(
            anime_id=20, content='test', recommendation='MF', author=testuser
        )

    def test_anime_page(self):
        c = Client()
        response = c.get('/anime/1')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['reviews'])
        self.assertIn(True, response.context['selected'].values())

    def test_profile_page(self):
        c = Client()
        response = c.get('/profile/testuser')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['reviews'].count(), 2)
        self.assertIn(True, response.context['selected'].values())

    def test_valid_like(self):
        c = Client()
        c.login(username='testuser', password='password')
        response = c.post('/like/1')
        review = Review.objects.get(id=1)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(review.likes.count(), 1)

    def test_valid_dislike(self):
        c = Client()
        c.login(username='testuser', password='password')
        response = c.post('/dislike/1')
        review = Review.objects.get(id=1)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(review.dislikes.count(), 1)