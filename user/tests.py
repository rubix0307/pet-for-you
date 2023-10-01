from django.test import TestCase, Client
from django.urls import reverse


class TestAuth(TestCase):

    def test_register(self):
        c = Client()

        data = {
            'first_name':'first_name',
            'last_name':'last_name',
            'email':'test_email@example.com',
            'password1':'password',
            'password2':'password',
            'registration_form':'', # to identify form processing
        }
        response = c.post(path=reverse('user_auth'), data=data)

        print(response.status_code)  # Просто для проверки статуса ответа
