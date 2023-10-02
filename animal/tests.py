import random
import unittest
import datetime as dt
from datetime import datetime
from django.urls import reverse
from django.test import TestCase, Client

from animal.models import Animal, Feedback
from user.models import CustomUser
from animal.utils import comb, get_available_pet_walk_time


class TestWalkSchedule(unittest.TestCase):
    walk_times = [
        (comb(8, 0), comb(8, 15)),
        (comb(9, 30), comb(10, 0)),
        (comb(10, 30), comb(11, 0)),
        (comb(11, 30), comb(12, 0)),
        (comb(12, 30), comb(13, 0)),
        (comb(13, 45), comb(14, 0)),
        (comb(14, 30), comb(15, 0)),
        (comb(16, 30), comb(17, 0)),
        (comb(17, 15), comb(17, 30)),
    ]
    selected_day = datetime.combine(datetime.now(), dt.time(hour=8))

    def test_duration_15(self):
        test_available_pet_walk_time = get_available_pet_walk_time(
            walk_times=self.walk_times,
            duration=15,
            selected_day=self.selected_day,
        )
        expected_result = [comb(8, 15),  comb(8, 30),
                  comb(8, 45),  comb(9, 0),
                  comb(9, 15),  comb(10, 0),
                  comb(10, 15), comb(11, 0),
                  comb(11, 15), comb(12, 0),
                  comb(12, 15), comb(13, 0),
                  comb(13, 15), comb(13, 30),
                  comb(14, 0),  comb(14, 15),
                  comb(15, 0),  comb(15, 15),
                  comb(15, 30), comb(15, 45),
                  comb(16, 0),  comb(16, 15),
                  comb(17, 0),  comb(17, 30),
                  comb(17, 45),]
        self.assertEqual(test_available_pet_walk_time, expected_result)

    def test_duration_30(self):
        test_available_pet_walk_time = get_available_pet_walk_time(
            walk_times=self.walk_times,
            duration=30,
            selected_day=self.selected_day,
        )
        expected_result = [comb(8, 15),  comb(8, 30),  comb(8, 45),  comb(9, 00),
                  comb(10, 00), comb(11, 00), comb(12, 00), comb(13, 00),
                  comb(13, 15), comb(14, 00), comb(15, 00), comb(15, 15),
                  comb(15, 30), comb(15, 45), comb(16, 00), comb(17, 30),]
        self.assertEqual(test_available_pet_walk_time, expected_result)

    def test_duration_60(self):
        test_available_pet_walk_time = get_available_pet_walk_time(
            walk_times=self.walk_times,
            duration=60,
            selected_day=self.selected_day,
        )
        expected_result = [comb(8, 15), comb(8, 30), comb(15, 00), comb(15, 15), comb(15, 30), ]
        self.assertEqual(test_available_pet_walk_time, expected_result)

    def test_duration_60_mixed(self):
        test_walk_times = self.walk_times[:]
        random.shuffle(test_walk_times)

        available_pet_walk_time = get_available_pet_walk_time(
            walk_times=test_walk_times,
            duration=60,
            selected_day=self.selected_day
        )
        expected_result = [comb(8, 15), comb(8, 30), comb(15, 00), comb(15, 15), comb(15, 30), ]
        self.assertEqual(available_pet_walk_time, expected_result)

    def test_not_selected_day(self):
        available_pet_walk_time = get_available_pet_walk_time(
            walk_times=self.walk_times,
            duration=60,
        )
        expected_result = [comb(8, 15), comb(8, 30), comb(15, 00), comb(15, 15), comb(15, 30), ]
        self.assertEqual(available_pet_walk_time, expected_result)

    def test_next_selected_day_and_empty_walk_times(self):
        selected_day = datetime.now() + dt.timedelta(days=1)
        next_selected_daty_walk = get_available_pet_walk_time(
            walk_times=self.walk_times,
            duration=60,
            selected_day=selected_day,
        )
        empty_walk_times = get_available_pet_walk_time(
            walk_times=[],
            duration=60,
            selected_day=selected_day,
        )

        expected_result = [comb(8, 0, selected_day), comb(8, 15, selected_day), comb(8, 30, selected_day), comb(8, 45, selected_day),
                  comb(9, 0, selected_day), comb(9, 15, selected_day), comb(9, 30, selected_day), comb(9, 45, selected_day),
                  comb(10, 0, selected_day), comb(10, 15, selected_day), comb(10, 30, selected_day), comb(10, 45, selected_day),
                  comb(11, 0, selected_day), comb(11, 15, selected_day), comb(11, 30, selected_day), comb(11, 45, selected_day),
                  comb(12, 0, selected_day), comb(12, 15, selected_day), comb(12, 30, selected_day), comb(12, 45, selected_day),
                  comb(13, 0, selected_day), comb(13, 15, selected_day), comb(13, 30, selected_day), comb(13, 45, selected_day),
                  comb(14, 0, selected_day), comb(14, 15, selected_day), comb(14, 30, selected_day), comb(14, 45, selected_day),
                  comb(15, 0, selected_day), comb(15, 15, selected_day), comb(15, 30, selected_day), comb(15, 45, selected_day),
                  comb(16, 0, selected_day), comb(16, 15, selected_day), comb(16, 30, selected_day), comb(16, 45, selected_day),
                  comb(17, 0,selected_day),]

        self.assertEqual(next_selected_daty_walk, expected_result)
        self.assertEqual(empty_walk_times, expected_result)

class TestFeedback(TestCase):
    fixtures = ["test_data.json"]

    def setUp(self):
        self.email = 'miroshnichenkoartem0307@gmail.com'
        self.password = '12345'

        self.c = Client()
        is_login = self.c.login(email=self.email, password=self.password)

        self.user = CustomUser.objects.filter(email=self.email).first()
        self.animal = Animal.objects.first()

    def test_correct_add(self):
        animal_feedbacks_count_before = len(Feedback.objects.filter(user=self.user, animal=self.animal).all())

        data_feedback = dict(
            title='title',
            text='text'
        )
        response = self.c.post(reverse('animal_feedback', kwargs={'animal_id': self.animal.id}), data=data_feedback)
        animal_feedbacks_count_after = len(Feedback.objects.filter(user=self.user, animal=self.animal).all())

        self.assertEquals(response.status_code, 302)
        self.assertEquals(animal_feedbacks_count_before + 1, animal_feedbacks_count_after)

    def test_incorrect_user(self):
        c = Client()

        animal_feedbacks_count_before = len(Feedback.objects.filter(animal=self.animal).all())

        data_feedback = dict(
            title='title',
            text='text'
        )
        response = c.post(reverse('animal_feedback', kwargs={'animal_id': self.animal.id}), data=data_feedback)
        animal_feedbacks_count_after = len(Feedback.objects.filter(animal=self.animal).all())

        self.assertEquals(response.status_code, 302)
        self.assertEquals(animal_feedbacks_count_before, animal_feedbacks_count_after)

    def test_incorrect_data(self):

        animal_feedbacks_count_before = len(Feedback.objects.filter(animal=self.animal).all())

        data_feedback = dict(
            title='',
            text=''
        )
        response = self.c.post(reverse('animal_feedback', kwargs={'animal_id': self.animal.id}), data=data_feedback)
        animal_feedbacks_count_after = len(Feedback.objects.filter(animal=self.animal).all())

        self.assertEquals(response.status_code, 302)
        self.assertEquals(animal_feedbacks_count_before, animal_feedbacks_count_after)

class TestRecordsSchedule(TestCase):
    fixtures = ["test_data.json"]

    def setUp(self):
        self.email = 'miroshnichenkoartem0307@gmail.com'
        self.password = '12345'

        self.c = Client()
        is_login = self.c.login(email=self.email, password=self.password)

        self.user = CustomUser.objects.filter(email=self.email).first()
        self.animal = Animal.objects.first()

    def test_write(self):
        pass

    def test_write_not_unique_date(self):
        pass