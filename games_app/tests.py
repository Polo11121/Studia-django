from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Game, Player, PlayerGameLink


class GameModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

        self.player = Player.objects.create(user=self.user)

        self.game = Game.objects.create(title='Test Game', genre='Puzzle')

    def test_game_creation(self):
        self.assertIsInstance(self.game, Game)
        self.assertEqual(self.game.title, 'Test Game')

    def test_average_score(self):
        PlayerGameLink.objects.create(game=self.game, player=self.player, score=8)

        self.game.refresh_from_db()
        self.assertEqual(self.game.average_score(), 8.0)


class ViewTestCase(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_signup_view(self):
        response = self.client.get(reverse('signUp'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signUp.html')


class SignUpFormTest(TestCase):
    def test_valid_signup_form(self):
        data = {'username': 'testuser', 'password1': 'testpassword123', 'password2': 'testpassword123'}
        response = self.client.post(reverse('signUp'), data)
        self.assertEqual(response.status_code, 302)  #

    def test_invalid_signup_form(self):
        data = {'username': 'testuser', 'password1': 'testpassword123', 'password2': 'wrongpassword'}
        response = self.client.post(reverse('signUp'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
