import time
from data import read
from data.model import Solution, Route
from helpers import *
from local_search import *

if __name__ == "__main__":

    # starting algorithm
    start_time = time.time()

    # reading data
    data = read.data

    # initial solution
    solution = Solution()
    solution.populate(data.vehicles)
    for job in data.jobs:
        closest_vehicle = get_closest_vehicle(solution.routes, data.vehicles, data.matrix, job)
        route = [x for x in solution.routes if x.vehicle_id == closest_vehicle.id][0]
        route.job_ids.append(job.id)
        route.load += job.delivery
    for route in solution.routes:
        route.update_duration(data)
    solution.update_duration()
    print('Total delivery duration of the initial solution: {0}'
          .format(solution.total_delivery_duration))

    # improve routes with local search
    solution = local_search(data, solution)
    print('Total delivery duration after local search: {0}'
          .format(solution.total_delivery_duration))

    # export solution
    solution.export('output.json')

    # algorithm completed
    print("Algorithm completed in %.3f seconds." %
          (time.time() - start_time))
