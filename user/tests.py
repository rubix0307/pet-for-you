from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser

class TestAuth(TestCase):

    def test_correct_register_login(self):
        c = Client()

        data_register = {
            'first_name':'first_name',
            'last_name':'last_name',
            'email':'test_register_login@example.com',
            'password1':'password',
            'password2':'password',
        }

        response_register = c.post(path=reverse('user_auth'), data=data_register)

        user = CustomUser.objects.filter(email=data_register['email']).first()
        self.assertEquals(type(user), CustomUser)
        self.assertEquals(response_register.status_code, 302)
        self.assertEquals(response_register.url, reverse('profile'))

        self.assertEqual(user.first_name, data_register['first_name'])
        self.assertEqual(user.last_name, data_register['last_name'])
        self.assertEqual(user.email, data_register['email'])

        data_login = {
            'email':'test_register_login@example.com',
            'password':'password',
        }

        response_login = c.post(path=reverse('user_auth'), data=data_login)
        self.assertTrue(response_login.wsgi_request.user.is_authenticated)
        self.assertEqual(response_login.status_code, 302)
        self.assertRedirects(response_login, reverse('profile'))

    def test_incorrect_login(self):
        c = Client()
        data_login = {
            'email': 'test_incorrect_login@example.com',
            'password': 'test_incorrect_login_password',
        }

        response_login = c.post(path=reverse('user_auth'), data=data_login)
        self.assertEqual(response_login.status_code, 200)
        self.assertFalse(response_login.wsgi_request.user.is_authenticated)
        self.assertContains(response_login,'Неверный email или пароль')

    def test_incorrect_register(self):
        # correct register
        c = Client()
        data_register = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'test_incorrect_register@example.com',
            'password1': 'password',
            'password2': 'password',
        }

        response_correct_register = c.post(path=reverse('user_auth'), data=data_register)
        user = CustomUser.objects.filter(email=data_register['email']).first()
        self.assertEquals(type(user), CustomUser)
        self.assertEquals(response_correct_register.status_code, 302)
        self.assertEquals(response_correct_register.url, reverse('profile'))

        # incorrect_register
        c = Client()

        data_register = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'test_incorrect_register@example.com',
            'password1': 'password',
            'password2': 'password-password',
        }

        response_register = c.post(path=reverse('user_auth'), data=data_register)
        self.assertContains(response_register, 'Пользователь с такой почтой уже зарегистрирован')
        self.assertContains(response_register, 'Пароли не совпадают')