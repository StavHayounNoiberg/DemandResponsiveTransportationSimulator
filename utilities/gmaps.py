import logging
import googlemaps
from datetime import datetime


logger = logging.getLogger(__name__)


# Replace with your own API key
API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'

# Initialize the Google Maps client
gmaps = googlemaps.Client(key='AIzaSyBh_8NtC_OKUtV381xzxxs3A6NmJie2IN8')


def get_route(leave_time: datetime, waypoints: list[tuple[float, float]], mode="driving") -> list[datetime]:
    if len(waypoints) < 2:
        logger.error("Not enough waypoints provided")
        return None

    start_coords = waypoints[0]
    end_coords = waypoints[-1]
    waypoints = waypoints[1:-1]

    # Request public transport directions with waypoints
    directions_result = gmaps.directions(start_coords,
                                         end_coords,
                                         mode=mode,
                                         waypoints=waypoints,
                                         departure_time=leave_time)

    # Extract and print the route length, duration, and time of arrival at each stop
    if directions_result:
        legs = directions_result[0]['legs']
        total_distance_meters = 0
        total_duration_seconds = 0

        for i, leg in enumerate(legs):
            total_distance_meters += leg['distance']['value']
            total_duration_seconds += leg['duration']['value']

            for step in leg['steps']:
                if 'transit_details' in step:
                    arrival_time = step['transit_details']['arrival_time']['text']
                    stop_name = step['transit_details']['arrival_stop']['name']
                    print(f"Arrival at {stop_name}: {arrival_time}")

        total_distance_km = total_distance_meters / 1000
        total_duration_minutes = total_duration_seconds / 60

        print(f"Route length: {total_distance_km:.2f} km")
        print(f"Route duration: {total_duration_minutes:.2f} minutes")
    else:
        print("No public transport route found.")

    # # Extract and print the route length, duration, and time of arrival at each stop
    # if directions_result:
    #     legs = directions_result[0]['legs']
    #     total_distance_meters = 0
    #     total_duration_seconds = 0

    #     for i, leg in enumerate(legs):
    #         total_distance_meters += leg['distance']['value']
    #         total_duration_seconds += leg['duration']['value']

    #         for step in leg['steps']:
    #             if 'transit_details' in step:
    #                 arrival_time = step['transit_details']['arrival_time']['text']


# # Define the coordinates for start, end points, and waypoints
# # Example: New York, Empire State Building
# start_coords = (40.748817, -73.985428)
# end_coords = (40.730610, -73.935242)    # Example: New York, Brooklyn
# waypoints = [
#     (40.752726, -73.977229),  # Example: New York, Grand Central Terminal
#     (40.741895, -73.989308)   # Example: New York, Flatiron Building
# ]

# # Request public transport directions with waypoints
# now = datetime.now()
# directions_result = gmaps.directions(start_coords,
#                                      end_coords,
#                                      mode="transit",
#                                      waypoints=waypoints,
#                                      departure_time=now)

# # # Extract and print the route length, duration, and time of arrival at each stop
# # if directions_result:
# #     legs = directions_result[0]['legs']
# #     total_distance_meters = 0
# #     total_duration_seconds = 0

# #     for i, leg in enumerate(legs):
# #         total_distance_meters += leg['distance']['value']
# #         total_duration_seconds += leg['duration']['value']

# #         for step in leg['steps']:
# #             if 'transit_details' in step:
# #                 arrival_time = step['transit_details']['arrival_time']['text']
# #                 stop_name = step['transit_details']['arrival_stop']['name']
# #                 print(f"Arrival at {stop_name}: {arrival_time}")

# #     total_distance_km = total_distance_meters / 1000
# #     total_duration_minutes = total_duration_seconds / 60

# #     print(f"Route length: {total_distance_km:.2f} km")
# #     print(f"Route duration: {total_duration_minutes:.2f} minutes")
# # else:
# #     print("No public transport route found.")
