import datetime
import datetime as dt
from typing import List, Tuple, Union
import unittest

def f_time(num:Union[int | str]):
    return num if int(num) > 9 else f'0{num}'

def round_minutes_to_nearest_value(d_time, value=15):
    minute = (d_time.minute + int(value/2)) // value * value
    if minute == 60:
        minute = 0
        d_time += dt.timedelta(hours=1)
    rounded_dt = d_time.replace(minute=minute, second=0, microsecond=0)
    return rounded_dt


def get_available_pet_walk_time(
        selected_day: dt.datetime,
        walk_times: List[Tuple[dt.datetime, dt.datetime]],
        duration_min:int,
        work_start_hour:int=8,
        work_end_hour:int=18):

    work_end = dt.datetime.now().replace(hour=work_end_hour, minute=0, second=0, microsecond=0)
    available_times = []

    current_time = round_minutes_to_nearest_value(
        selected_day.replace(hour=selected_day.hour if work_start_hour <= selected_day.hour else work_start_hour)
    )

    while current_time + dt.timedelta(minutes=duration_min) <= work_end:

        is_available = True
        for walk_time in walk_times:

            if walk_time[0] <= current_time < walk_time[1]:
                is_available = False
                break

        if is_available:
            available_times.append(f'{f_time(current_time.hour)}:{f_time(current_time.minute)}')

        current_time += dt.timedelta(minutes=duration_min)

    return available_times

def get_available_pet_walk_time2(
        booked_time_frames,
        min_time_slot_in_minutes: int = 15,
        selected_day: None | dt.datetime = None,
        work_start_in_hour=8,
        work_end_in_hour=18,
):
    if not selected_day:
        selected_day = dt.datetime.now()

    min_time_slot = dt.timedelta(minutes=min_time_slot_in_minutes)
    open_time = dt.datetime.combine(selected_day, dt.time(hour=work_start_in_hour))
    close_time = dt.datetime.combine(selected_day, dt.time(hour=work_end_in_hour))

    booked_time_slots = []
    all_time_slots = []

    while open_time <= close_time - min_time_slot:
        all_time_slots.append(open_time.strftime('%H:%M'))
        open_time += min_time_slot

    for start_time, end_time in booked_time_frames:
        while start_time < end_time:
            booked_time_slots.append(start_time.strftime('%H:%M'))
            start_time += min_time_slot

    available_times = sorted(set(all_time_slots) - set(booked_time_slots))
    return available_times


booked_time_frames = [
    (dt.datetime(2023, 9, 21, 8, 0), dt.datetime(2023, 9, 21, 8, 15)),
    (dt.datetime(2023, 9, 21, 8, 15), dt.datetime(2023, 9, 21, 8, 30)),
    (dt.datetime(2023, 9, 21, 9, 0), dt.datetime(2023, 9, 21, 9, 45)),
    (dt.datetime(2023, 9, 21, 10, 0), dt.datetime(2023, 9, 21, 10, 30)),
]

available_times2 = get_available_pet_walk_time2(
     booked_time_frames=booked_time_frames,
     min_time_slot_in_minutes=15,
     selected_day=dt.datetime(2023, 9, 28),
     work_start_in_hour=8,
     work_end_in_hour=18,
)


class TestAvailablePetWalkTime(unittest.TestCase):

    def test_1_booked_time_frames_small(self):
        booked_time_frames = []

        available_pet_walk_time = get_available_pet_walk_time2(
            booked_time_frames=booked_time_frames,
            min_time_slot_in_minutes=15,
            selected_day=dt.datetime(2023, 9, 28),
            work_start_in_hour=8,
            work_end_in_hour=18,
        )
        container = ['08:00', '08:15', '08:30', '08:45', '09:00','09:15', '09:30',
                     '09:45', '10:00', '10:15', '10:30', '10:45','11:00', '11:15',
                     '11:30', '11:45', '12:00', '12:15', '12:30','12:45', '13:00',
                     '13:15', '13:30', '13:45', '14:00', '14:15','14:30', '14:45',
                     '15:00', '15:15', '15:30', '15:45', '16:00','16:15', '16:30',
                     '16:45', '17:00', '17:15', '17:30', '17:45']
        self.assertEqual(available_pet_walk_time, container)

    def test_2_booked_time_frames_medium(self):
        booked_time_frames = [
            (dt.datetime(2023, 9, 28, 8, 0), dt.datetime(2023, 9, 28, 8, 15)),
            (dt.datetime(2023, 9, 28, 8, 15), dt.datetime(2023, 9, 28, 8, 30)),
            (dt.datetime(2023, 9, 28, 9, 0), dt.datetime(2023, 9, 28, 9, 45)),
            (dt.datetime(2023, 9, 28, 10, 0), dt.datetime(2023, 9, 28, 10, 30)),
        ]
        available_pet_walk_time = get_available_pet_walk_time2(
            booked_time_frames=booked_time_frames,
            min_time_slot_in_minutes=15,
            selected_day=dt.datetime(2023, 9, 28),
            work_start_in_hour=8,
            work_end_in_hour=18,
        )
        container = ['08:30', '08:45', '09:45', '10:30', '10:45', '11:00', '11:15',
                     '11:30', '11:45', '12:00', '12:15', '12:30', '12:45', '13:00',
                     '13:15', '13:30', '13:45', '14:00', '14:15', '14:30', '14:45',
                     '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30',
                     '16:45', '17:00', '17:15', '17:30', '17:45']
        self.assertEqual(available_pet_walk_time, container)

    def test_3_booked_time_frames_medium_mixed(self):
        booked_time_frames = [
            (dt.datetime(2023, 9, 28, 9, 0), dt.datetime(2023, 9, 28, 9, 45)),
            (dt.datetime(2023, 9, 28, 10, 0), dt.datetime(2023, 9, 28, 10, 30)),
            (dt.datetime(2023, 9, 28, 8, 0), dt.datetime(2023, 9, 28, 8, 15)),
            (dt.datetime(2023, 9, 28, 8, 15), dt.datetime(2023, 9, 28, 8, 30)),
        ]
        available_pet_walk_time = get_available_pet_walk_time2(
            booked_time_frames=booked_time_frames,
            min_time_slot_in_minutes=15,
            selected_day=dt.datetime(2023, 9, 28),
            work_start_in_hour=8,
            work_end_in_hour=18,
        )
        container = ['08:30', '08:45', '09:45', '10:30', '10:45', '11:00', '11:15',
                     '11:30', '11:45', '12:00', '12:15', '12:30', '12:45', '13:00',
                     '13:15', '13:30', '13:45', '14:00', '14:15', '14:30', '14:45',
                     '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30',
                     '16:45', '17:00', '17:15', '17:30', '17:45']
        self.assertEqual(available_pet_walk_time, container)

    def test_4_booked_time_frames_large_and_last_slot(self):
        booked_time_frames = [
            (dt.datetime(2023, 9, 28, 8, 0), dt.datetime(2023, 9, 28, 8, 15)),
            (dt.datetime(2023, 9, 28, 8, 15), dt.datetime(2023, 9, 28, 8, 30)),
            (dt.datetime(2023, 9, 28, 8, 30), dt.datetime(2023, 9, 28, 8, 45)),
            (dt.datetime(2023, 9, 28, 8, 45), dt.datetime(2023, 9, 28, 9, 0)),
            (dt.datetime(2023, 9, 28, 9, 0), dt.datetime(2023, 9, 28, 9, 15)),
            (dt.datetime(2023, 9, 28, 9, 15), dt.datetime(2023, 9, 28, 9, 30)),
            (dt.datetime(2023, 9, 28, 9, 30), dt.datetime(2023, 9, 28, 9, 45)),
            (dt.datetime(2023, 9, 28, 9, 45), dt.datetime(2023, 9, 28, 10, 0)),
            (dt.datetime(2023, 9, 28, 10, 0), dt.datetime(2023, 9, 28, 10, 15)),
            (dt.datetime(2023, 9, 28, 10, 15), dt.datetime(2023, 9, 28, 10, 30)),
            (dt.datetime(2023, 9, 28, 10, 30), dt.datetime(2023, 9, 28, 10, 45)),
            (dt.datetime(2023, 9, 28, 10, 45), dt.datetime(2023, 9, 28, 11, 0)),
            (dt.datetime(2023, 9, 28, 11, 0), dt.datetime(2023, 9, 28, 11, 15)),
            (dt.datetime(2023, 9, 28, 11, 15), dt.datetime(2023, 9, 28, 11, 30)),
            (dt.datetime(2023, 9, 28, 11, 30), dt.datetime(2023, 9, 28, 11, 45)),
            (dt.datetime(2023, 9, 28, 11, 45), dt.datetime(2023, 9, 28, 12, 0)),
            (dt.datetime(2023, 9, 28, 12, 0), dt.datetime(2023, 9, 28, 12, 15)),
            (dt.datetime(2023, 9, 28, 12, 15), dt.datetime(2023, 9, 28, 12, 30)),
            (dt.datetime(2023, 9, 28, 12, 30), dt.datetime(2023, 9, 28, 12, 45)),
            (dt.datetime(2023, 9, 28, 12, 45), dt.datetime(2023, 9, 28, 13, 0)),
            (dt.datetime(2023, 9, 28, 13, 0), dt.datetime(2023, 9, 28, 13, 15)),
            (dt.datetime(2023, 9, 28, 13, 15), dt.datetime(2023, 9, 28, 13, 30)),
            (dt.datetime(2023, 9, 28, 13, 30), dt.datetime(2023, 9, 28, 13, 45)),
            (dt.datetime(2023, 9, 28, 13, 45), dt.datetime(2023, 9, 28, 14, 0)),
            (dt.datetime(2023, 9, 28, 14, 0), dt.datetime(2023, 9, 28, 14, 15)),
            (dt.datetime(2023, 9, 28, 14, 15), dt.datetime(2023, 9, 28, 14, 30)),
            (dt.datetime(2023, 9, 28, 14, 30), dt.datetime(2023, 9, 28, 14, 45)),
            (dt.datetime(2023, 9, 28, 14, 45), dt.datetime(2023, 9, 28, 15, 0)),
            (dt.datetime(2023, 9, 28, 15, 0), dt.datetime(2023, 9, 28, 15, 15)),
            (dt.datetime(2023, 9, 28, 15, 15), dt.datetime(2023, 9, 28, 15, 30)),
            (dt.datetime(2023, 9, 28, 15, 30), dt.datetime(2023, 9, 28, 15, 45)),
            (dt.datetime(2023, 9, 28, 15, 45), dt.datetime(2023, 9, 28, 16, 0)),
            (dt.datetime(2023, 9, 28, 16, 0), dt.datetime(2023, 9, 28, 16, 15)),
            (dt.datetime(2023, 9, 28, 16, 15), dt.datetime(2023, 9, 28, 16, 30)),
            (dt.datetime(2023, 9, 28, 16, 30), dt.datetime(2023, 9, 28, 16, 45)),
            (dt.datetime(2023, 9, 28, 16, 45), dt.datetime(2023, 9, 28, 17, 0)),
            (dt.datetime(2023, 9, 28, 17, 0), dt.datetime(2023, 9, 28, 17, 15)),
            (dt.datetime(2023, 9, 28, 17, 15), dt.datetime(2023, 9, 28, 17, 30)),
            (dt.datetime(2023, 9, 28, 17, 30), dt.datetime(2023, 9, 28, 17, 45)),
        ]
        available_pet_walk_time = get_available_pet_walk_time2(
            booked_time_frames=booked_time_frames,
            min_time_slot_in_minutes=15,
            selected_day=dt.datetime(2023, 9, 28),
            work_start_in_hour=8,
            work_end_in_hour=18,
        )
        container = ['17:45']
        self.assertEqual(available_pet_walk_time, container)

    def test_5_min_time_slot_in_minutes_30(self):
        booked_time_frames = []

        available_pet_walk_time = get_available_pet_walk_time2(
            booked_time_frames=booked_time_frames,
            min_time_slot_in_minutes=30,
            selected_day=dt.datetime(2023, 9, 28),
            work_start_in_hour=8,
            work_end_in_hour=18,
        )
        container = ['08:00', '08:30', '09:00', '09:30', '10:00',
                     '10:30', '11:00', '11:30', '12:00', '12:30',
                     '13:00', '13:30', '14:00', '14:30', '15:00',
                     '15:30', '16:00', '16:30', '17:00', '17:30']

        self.assertEqual(available_pet_walk_time, container)

    def test_6_min_time_slot_in_minutes_60(self):
        booked_time_frames = []

        available_pet_walk_time = get_available_pet_walk_time2(
            booked_time_frames=booked_time_frames,
            min_time_slot_in_minutes=60,
            selected_day=dt.datetime(2023, 9, 28),
            work_start_in_hour=8,
            work_end_in_hour=18,
        )
        container = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']

        self.assertEqual(available_pet_walk_time, container)

    def test_7_not_selected_day(self):
        booked_time_frames = []

        available_pet_walk_time = get_available_pet_walk_time2(
            booked_time_frames=booked_time_frames,
            min_time_slot_in_minutes=60,
            work_start_in_hour=8,
            work_end_in_hour=18,
        )
        container = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']

        self.assertEqual(available_pet_walk_time, container)
