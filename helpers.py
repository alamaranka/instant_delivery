import math
import sys


def get_closest_vehicle(routes, vehicles, matrix, job):
    duration = sys.maxsize
    vehicle_s = None
    for vehicle in vehicles:
        load = [v for v in routes if v.vehicle_id == vehicle.id][0].load
        c_duration = matrix[vehicle.start_index][job.location_index]
        if c_duration < duration and load + job.delivery <= vehicle.capacity:
            duration = c_duration
            vehicle_s = vehicle
    return vehicle_s


def route_distance(matrix, location_indices):
    distance = 0
    for i in range(1, len(location_indices)):
        distance += matrix[location_indices[i-1]][location_indices[i]]
    return distance
