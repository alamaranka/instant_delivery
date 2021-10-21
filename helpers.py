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


def insert_job_to_route(data, route, index, job):
    route.load += job.delivery
    route.job_ids.insert(index, job.id)
    route.update_duration(data)
    return route


def generate_initial_solution(data, solution):
    solution.populate(data.vehicles)
    for job in data.jobs:
        closest_vehicle = get_closest_vehicle(solution.routes, data.vehicles, data.matrix, job)
        route = [x for x in solution.routes if x.vehicle_id == closest_vehicle.id][0]
        route.job_ids.append(job.id)
        route.load += job.delivery
    for route in solution.routes:
        route.update_duration(data)
    solution.update_duration()
    print('Total delivery duration of the initial solution: {0} seconds.'
          .format(solution.total_delivery_duration))
    return solution
