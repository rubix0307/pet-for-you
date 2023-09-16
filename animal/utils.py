import datetime as dt
from typing import List


def round_minutes_to_nearest_value(d_time, value=15):
    minute = (d_time.minute + int(value/2)) // value * value
    rounded_dt = d_time.replace(minute=minute, second=0, microsecond=0)
    return rounded_dt

def get_available_pet_walk_time(walk_times: List[dt.datetime], quarters: int, min_start_walk_hour=8, max_end_walk_hour=18):
    if len(walk_times) == 2 and quarters > 0:

        start_walk, end_walk = walk_times
        start_walk = start_walk if start_walk.hour >= min_start_walk_hour else start_walk.replace(hour=min_start_walk_hour, minute=0)
        end_walk = end_walk if end_walk.hour <= max_end_walk_hour else end_walk.replace(hour=max_end_walk_hour, minute=0)

        if start_walk.hour >= min_start_walk_hour:
            quarter_time = 15
            walking_time = quarters * quarter_time
            last_booking = end_walk - dt.timedelta(minutes=walking_time)

            available_pet_walk_time = []
            while last_booking >= start_walk:
                formatted_minutes = last_booking.minute if last_booking.minute > 9 else f'0{last_booking.minute}'
                available_pet_walk_time.append(f'{last_booking.hour}:{formatted_minutes}')
                last_booking -= dt.timedelta(minutes=quarter_time)

            return available_pet_walk_time[::-1]
    else:
        return []


walk_times = [
    round_minutes_to_nearest_value(dt.datetime(2023, 8, 1, 7, 8)),
    round_minutes_to_nearest_value(dt.datetime(2023, 8, 1, 9, 1)),
]
for i in range(-1, 5):
    print(i, get_available_pet_walk_time(walk_times, i))

print()

walk_times = [
    round_minutes_to_nearest_value(dt.datetime(2023, 8, 1, 17, 4)),
    round_minutes_to_nearest_value(dt.datetime(2023, 8, 1, 22, 6)),
]
for i in range(-1, 5):
    print(i, get_available_pet_walk_time(walk_times, i))
