import logging
import googlemaps
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


# Replace with your own API key
API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'

# Initialize the Google Maps client
gmaps = googlemaps.Client(key='AIzaSyBh_8NtC_OKUtV381xzxxs3A6NmJie2IN8')


def get_route_timedeltas(leave_time: datetime, waypoints: list[tuple[float, float]], mode="driving") -> list[timedelta]:

    timedeltas: list[timedelta] = [timedelta(seconds=0)]

    departure_time = leave_time
    if departure_time < datetime.now():
        diff = datetime.now() - departure_time
        weeks_to_add = (diff.days // 7) + 1
        departure_time += timedelta(weeks=weeks_to_add)

    if len(waypoints) < 2:
        logger.error("Not enough waypoints provided")
        return None

    start_coords = waypoints[0]
    end_coords = waypoints[-1]
    waypoints = waypoints[1:-1]

    try:
        # Request public transport directions with waypoints
        directions_result = gmaps.directions(start_coords,
                                             end_coords,
                                             mode=mode,
                                             waypoints=waypoints,
                                             departure_time=departure_time)

        # Extract and print the route length, duration, and time of arrival at each stop
        if directions_result:
            legs = directions_result[0]['legs']
            total_duration_seconds = 0

            for _, leg in enumerate(legs):
                total_duration_seconds += leg['duration']['value']
                timedeltas.append(timedelta(seconds=total_duration_seconds))
                
            return timedeltas

        else:
            raise Exception("No directions found")

    except Exception as e:
        logger.error(e)
        return None


def get_route(leave_time: datetime, waypoints: list[tuple[float, float]], mode="driving") -> list[timedelta]:
    timedeltas = get_route_timedeltas(leave_time, waypoints, mode)
    if timedeltas is None:
        return None

    datetimes = [leave_time + delta for delta in timedeltas]
    return datetimes
