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


def create_report_datetime(arrival_time: datetime):
    t = np.linspace(-168, 2, 1000)
    cdf = __customer_arrival_cdf(t)
    random_value = np.random.rand()
    report_time = np.interp(random_value, cdf, t)
    return arrival_time + timedelta(hours=report_time)


def __customer_arrival_dist(t):
    peak_time = -12
    peak_height = 0.2
    late_perc = 0.1
    weekly_increase = 0.5

    main_curve = peak_height * np.exp(-(t - peak_time) ** 2 / (2 * (peak_time / 3) ** 2))
    main_curve *= (1 + np.maximum(0, t / 168) * weekly_increase)
    late_curve = late_perc * peak_height * np.exp(-(t - 0.5) ** 2 / (2 * (0.25) ** 2))
    late_curve[t < 0] = 0
    pdf = main_curve + late_curve
    pdf /= np.trapz(pdf, t)
    return pdf


def __customer_arrival_cdf(t):
    pdf = __customer_arrival_dist(t)
    cdf = np.cumsum(pdf) * (t[1] - t[0])
    return cdf

