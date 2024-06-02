from datetime import datetime, timedelta
import numpy as np
import random


def create_datetimes_poisson_distribution(
    lambda_params: list[int], start_time: datetime, end_time: datetime
) -> list[datetime]:
    datetimes: list[datetime] = []
    hours: list[datetime] = []
    current_time = start_time
    while current_time < end_time:
        hours.append(current_time)
        current_time = current_time.replace(minute=0) + timedelta(hours=1)
    hours.append(end_time)

    for i in range(len(hours) - 1):
        current_hour = hours[i]
        next_hour = hours[i + 1]
        if 0 >= current_hour.hour < 5:
            continue  # Skip times between 12AM to 5AM

        hour_lambda = lambda_params[current_hour.hour]
        if hour_lambda == 0:
            continue

        num_events = np.random.poisson(hour_lambda)
        inter_arrival_times = np.random.exponential(
            scale=1 / hour_lambda, size=num_events)

        current_event_time = current_hour
        for inter_arrival_time in inter_arrival_times:
            event_time = current_event_time + \
                timedelta(hours=inter_arrival_time)
            if event_time > next_hour:
                break
            datetimes.append(event_time.replace(microsecond=0))
            current_event_time = event_time

    return datetimes


def create_datetimes_random(num_events: int, start_time: datetime, end_time: datetime):
    event_times = []
    delta_seconds = (end_time - start_time).total_seconds()

    events_generated = 0
    while events_generated < num_events:
        # Generate a random timedelta within the range
        random_delta = random.randint(0, int(delta_seconds))
        # Create a random datetime within the range
        random_time = start_time + timedelta(seconds=random_delta)

        # Check if the random time falls between 12AM to 5AM
        if not (0 <= random_time.hour < 6) and (random_time < end_time):
            event_times.append(random_time.replace(microsecond=0))
            events_generated += 1

    return event_times
