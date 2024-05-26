from datetime import datetime, timedelta
import numpy as np
import random


def create_datetimes_poisson_distribution(
    lambda_params: list[int], start_time: datetime, end_time: datetime
) -> list[datetime]:

    datetimes = []

    current_time = start_time
    while current_time < end_time:
        if 0 >= current_time.hour < 5:
            current_time += timedelta(hours=1)
            continue  # Skip times between 12AM to 5AM

        hour_lambda = lambda_params[current_time.hour]
        if hour_lambda == 0:
            current_time += timedelta(hours=1)
            continue

        events_in_hour = np.random.poisson(hour_lambda)

        # calculate the fraction of an hour from the current time to the next hour
        fraction_of_hour = (
            current_time + timedelta(hours=1) - current_time
        ).total_seconds() / 3600
        if (end_time - current_time).total_seconds() / 3600 < 1:
            fraction_of_hour = (end_time - current_time).total_seconds() / 3600

        num_events = int(events_in_hour * fraction_of_hour)
        inter_arrival_times = np.random.exponential(
            scale=1 / hour_lambda, size=num_events
        )
        for inter_arrival_time in inter_arrival_times:
            event_time = current_time + timedelta(hours=inter_arrival_time)
            if event_time > end_time:
                break
            datetimes.append(event_time.replace(microsecond=0))

        current_time += timedelta(hours=1)

    return datetimes

    # # Calculate the total duration
    # total_duration_hours = (end_time - start_time).total_seconds() / 3600  # in hours

    # # Generate the number of events occurring in each hour within the specified duration
    # event_counts_per_hour = np.random.poisson(lambda_param, int(total_duration_hours))

    # # Generate datetime objects for event occurrences
    # event_times = []
    # for hour, count in enumerate(event_counts_per_hour):
    #     current_hour = start_time + timedelta(hours=hour)
    #     if 0 >= current_hour.hour < 5:
    #         continue  # Skip times between 12AM to 5AM
    #     if count == 0:
    #         continue
    #     # Generate random inter-arrival times (exponential distribution)
    #     inter_arrival_times = np.random.exponential(scale=1 / lambda_param, size=count)
    #     # Convert inter-arrival times to datetime objects
    #     for inter_arrival_time in inter_arrival_times:
    #         event_time = current_hour + timedelta(hours=inter_arrival_time)
    #         if event_time > end_time:
    #             break
    #         event_times.append(event_time.replace(microsecond=0))

    # return event_times


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
