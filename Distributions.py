from datetime import datetime, timedelta
from enum import Enum
import numpy as np
import random


class DistributionTypes(Enum):
    POISSON = 1
    RANDOM = 2
    EMPIRIC = 3


class Distributions:

    def create_event_times_poisson(
        lambda_param: int, start_time: datetime, end_time: datetime
    ):

        # Calculate the total duration
        total_duration_hours = (
            end_time - start_time
        ).total_seconds() / 3600  # in hours

        # Generate the number of events occurring in each hour within the specified duration
        event_counts_per_hour = np.random.poisson(
            lambda_param, int(total_duration_hours)
        )

        # Generate datetime objects for event occurrences
        event_times = []
        for hour, count in enumerate(event_counts_per_hour):
            current_hour = start_time + timedelta(hours=hour)
            if 0 >= current_hour.hour < 5:
                continue  # Skip times between 12AM to 5AM
            if count == 0:
                continue
            # Generate random inter-arrival times (exponential distribution)
            inter_arrival_times = np.random.exponential(
                scale=1 / lambda_param, size=count
            )
            # Convert inter-arrival times to datetime objects
            for inter_arrival_time in inter_arrival_times:
                event_time = current_hour + timedelta(hours=inter_arrival_time)
                if event_time > end_time:
                    break
                event_times.append(event_time.replace(microsecond=0))

        return event_times

    def create_event_times_random(
        num_events: int, start_time: datetime, end_time: datetime
    ):
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

    def create_event_times_empiric():
        # TODO: Create empiric distribution
        pass
