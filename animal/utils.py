import datetime as dt
from typing import List, Tuple, Union

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


# selected_day = dt.datetime(2023, 9, 21, 8, 0)
# walk_times = [
#     (dt.datetime(2023, 9, 21, 8, 0), dt.datetime(2023, 9, 21, 8, 15)),
#     (dt.datetime(2023, 9, 21, 8, 15), dt.datetime(2023, 9, 21, 8, 30)),
#     (dt.datetime(2023, 9, 21, 9, 0), dt.datetime(2023, 9, 21, 9, 45)),
#     (dt.datetime(2023, 9, 21, 10, 0), dt.datetime(2023, 9, 21, 10, 30)),
# ]
#
# available_times = get_available_pet_walk_time(
#     selected_day,
#     walk_times,
#     duration_min=15,
#     work_start_hour=8,
#     work_end_hour=11)
# print(available_times)
