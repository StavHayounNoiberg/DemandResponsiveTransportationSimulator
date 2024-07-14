import logging
import googlemaps
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


# Replace with your own API key
API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=API_KEY)


def __get_route_timedeltas(leave_time: datetime, waypoints: list[tuple[float, float]], mode="driving") -> list[timedelta]:

    timedeltas: list[timedelta] = [timedelta(seconds=0)]

    departure_time = leave_time
    if departure_time < datetime.now():
        diff = datetime.now() - departure_time
        weeks_to_add = (diff.days // 7) + 1
        departure_time += timedelta(weeks=weeks_to_add)

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


def get_route(leave_time: datetime, waypoints: list[tuple[float, float]], mode="driving") -> list[datetime]:
    if len(waypoints) < 2:
        logger.error("Not enough waypoints provided")
        return None
    
    datetimes: list[datetime] = []
    last_time = leave_time
    for i in range(0, len(waypoints), 25):
        segment_waypoints = []
        if i == 0:
            segment_waypoints = waypoints[i:i+25]
        else:
            segment_waypoints = waypoints[i-1:i+25]
        timedeltas = __get_route_timedeltas(last_time, segment_waypoints, mode)
        if timedeltas is None:
            return None
        
        if i > 0:
            timedeltas = timedeltas[1:]
        datetimes.extend([last_time + delta for delta in timedeltas])
        last_time = datetimes[-1]
    
    return datetimes


def get_route_timedeltas(leave_time: datetime, waypoints: list[tuple[float, float]], mode="driving") -> list[timedelta]:
    if len(waypoints) < 2:
        logger.error("Not enough waypoints provided")
        return None

    timedeltas: list[timedelta] = []
    last_time = leave_time

    for i in range(0, len(waypoints), 25):
        segment_waypoints = []
        if i == 0:
            segment_waypoints = waypoints[i:i+25]
        else:
            segment_waypoints = waypoints[i-1:i+25]
        route_timedeltas = __get_route_timedeltas(last_time, segment_waypoints, mode)
        if route_timedeltas is None:
            return None
        
        last_time += route_timedeltas[-1]
        if i > 0:
            route_timedeltas = [time + timedeltas[-1] for time in route_timedeltas[1:]]
        timedeltas.extend(route_timedeltas)        
    
    # Compute the differences between consecutive stops
    timedeltas_between_stops = [timedeltas[0]]
    for j in range(1, len(timedeltas)):
        timedeltas_between_stops.append(timedeltas[j] - timedeltas[j-1])

    return timedeltas_between_stops

