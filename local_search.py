from helpers import *
from data.model import Route


def two_opt(data, route, output_log):
    for i in range(len(route.job_ids) - 1):
        for j in range(i + 1, len(route.job_ids)):
            new_job_order = []
            new_job_order += route.job_ids[0:i]
            new_job_order += route.job_ids[i:j + 1][::-1]
            new_job_order += route.job_ids[j + 1:len(route.job_ids)]
            new_route = Route(vehicle_id=route.vehicle_id)
            new_route.job_ids = new_job_order
            new_route.update_duration(data)
            if new_route.delivery_duration < route.delivery_duration:
                improvement = route.delivery_duration - new_route.delivery_duration
                route.job_ids = new_route.job_ids
                route.delivery_duration = new_route.delivery_duration
                if output_log:
                    print('Two-Opt operator improvement\t-> {0}'.format(improvement))
                return True
    return False


def apply_two_opt(data, routes):
    for route in routes:
        improved = True
        while improved:
            improved = two_opt(data, route, True)


def exchange(data, routes):
    for r1 in range(len(routes)):
        for r2 in range(len(routes)):
            if r1 != r2:
                route1 = routes[r1]
                route2 = routes[r2]
                for j1 in range(len(route1.job_ids)):
                    for j2 in range(len(route2.job_ids)):
                        # get jobs to exchange
                        job1 = [v for v in data.jobs if v.id == route1.job_ids[j1]][0]
                        job2 = [v for v in data.jobs if v.id == route2.job_ids[j2]][0]
                        # create copies of routes
                        route1_copy = route1.copy()
                        route2_copy = route2.copy()
                        # remove jobs from their current routes
                        job1_index = route1_copy.job_ids.index(job1.id)
                        job2_index = route2_copy.job_ids.index(job2.id)
                        route1_copy.job_ids.remove(job1.id)
                        route2_copy.job_ids.remove(job2.id)
                        route1_copy.load -= job1.delivery
                        route2_copy.load -= job2.delivery
                        # prepare new routes
                        # insert job1 to route2
                        route1_copy = insert_job_to_route(data, route1_copy, job1_index, job2)
                        route2_copy = insert_job_to_route(data, route2_copy, job2_index, job1)
                        # get necessary info
                        new_total_delivery_duration = route1_copy.delivery_duration + route2_copy.delivery_duration
                        current_total_delivery_duration = route1.delivery_duration + route2.delivery_duration
                        route1_vehicle_capacity = [v for v in data.vehicles if v.id == route1.vehicle_id][0].capacity
                        route2_vehicle_capacity = [v for v in data.vehicles if v.id == route2.vehicle_id][0].capacity
                        if new_total_delivery_duration < current_total_delivery_duration and \
                                route1_copy.load <= route1_vehicle_capacity and \
                                route2_copy.load <= route2_vehicle_capacity:
                            improvement = current_total_delivery_duration - new_total_delivery_duration
                            route1.job_ids = route1_copy.job_ids
                            route1.delivery_duration = route1_copy.delivery_duration
                            route1.load = route1_copy.load
                            route2.job_ids = route2_copy.job_ids
                            route2.delivery_duration = route2_copy.delivery_duration
                            route2.load = route2_copy.load
                            print('Exchange operator improvement\t-> {0}'.format(improvement))
                            return True
    return False


def apply_exchange(data, routes):
    improved = True
    while improved:
        improved = exchange(data, routes)


def relocate(data, routes):
    for r1 in range(len(routes)):
        for r2 in range(len(routes)):
            if r1 != r2:
                route1 = routes[r1]
                route2 = routes[r2]
                for j1 in range(len(route1.job_ids)):
                    for j2 in range(len(route2.job_ids)):
                        # get job to relocate
                        job1 = [v for v in data.jobs if v.id == route1.job_ids[j1]][0]
                        # create copies of routes
                        route1_copy = route1.copy()
                        route2_copy = route2.copy()
                        # remove job from its current route
                        job1_index = route1_copy.job_ids.index(job1.id)
                        route1_copy.job_ids.remove(job1.id)
                        route1_copy.load -= job1.delivery
                        # prepare new routes
                        # insert job1 to route2
                        route2_copy = insert_job_to_route(data, route2_copy, 0, job1)
                        # apply two-opt on new route
                        improved = True
                        while improved:
                            improved = two_opt(data, route2_copy, False)
                        # get necessary info
                        new_total_delivery_duration = route1_copy.delivery_duration + route2_copy.delivery_duration
                        current_total_delivery_duration = route1.delivery_duration + route2.delivery_duration
                        route1_vehicle_capacity = [v for v in data.vehicles if v.id == route1.vehicle_id][0].capacity
                        route2_vehicle_capacity = [v for v in data.vehicles if v.id == route2.vehicle_id][0].capacity
                        if new_total_delivery_duration < current_total_delivery_duration and \
                                route1_copy.load <= route1_vehicle_capacity and \
                                route2_copy.load <= route2_vehicle_capacity:
                            improvement = current_total_delivery_duration - new_total_delivery_duration
                            route1.job_ids = route1_copy.job_ids
                            route1.delivery_duration = route1_copy.delivery_duration
                            route1.load = route1_copy.load
                            route2.job_ids = route2_copy.job_ids
                            route2.delivery_duration = route2_copy.delivery_duration
                            route2.load = route2_copy.load
                            print('Relocate operator improvement\t-> {0}'.format(improvement))
                            return True
    return False


def apply_relocate(data, routes):
    improved = True
    while improved:
        improved = relocate(data, routes)


def local_search(data, solution):
    improved = True
    while improved:
        improved = False
        total_delivery_duration = solution.total_delivery_duration
        apply_two_opt(data, solution.routes)
        apply_exchange(data, solution.routes)
        apply_relocate(data, solution.routes)
        solution.update_duration()
        improved |= solution.total_delivery_duration < total_delivery_duration
    solution.update_duration()
    return solution
