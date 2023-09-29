import datetime as dt
from datetime import datetime, timedelta
from typing import List, Union

def comb(hour, minute, day: datetime=datetime.now()):
    return datetime.combine(day, dt.time(hour=hour, minute=minute))

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
        walk_times:List[datetime],
        selected_day=datetime.now(),
        duration=15,
        start_hour=8,
        end_hour=18,
):
    step_minutes = 15
    duration_in_steps = duration / step_minutes
    walk_times = [wt for wt in walk_times if wt[0].month == selected_day.month and wt[0].day == selected_day.day]
    start = datetime.combine(selected_day, dt.time(hour=start_hour))
    end = datetime.combine(selected_day, dt.time(hour=end_hour))

    walk_times_starts = [w[0] for w in walk_times]

    day_slots = []

    cursor = start.replace()
    while cursor < end:
        day_slots.append(cursor)
        cursor += timedelta(minutes=step_minutes)
    day_slots.append(end)

    for walk_start, walk_end in walk_times:
        cursor = walk_start.replace()
        if cursor.month == start.month and cursor.day == start.day:
            while cursor < walk_end:
                day_slots.pop(day_slots.index(cursor))
                cursor += timedelta(minutes=step_minutes)

    available_slots = []

    line = day_slots[:]
    start_cursor = line[0]
    while start_cursor < end:
        steps = 0
        start_cursor = line[0]

        for n, slot in enumerate(line):
            try:
                next_slot = slot + timedelta(minutes=step_minutes)
                if next_slot == line[n+1] or next_slot in walk_times_starts:
                    if not start_cursor in available_slots:
                        steps += 1
                        if steps == duration_in_steps:
                            available_slots.append(start_cursor)
                            line = line[1:]
                            break
                    if next_slot in walk_times_starts:
                        line = line[1:]
                        break
            except IndexError:
                start_cursor = end
                break

    return available_slots

