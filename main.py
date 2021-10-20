from data import read
from data.model import Solution, Route
from helpers import *

data = read.data
n_vehicles = len(data.vehicles)
n_jobs = len(data.jobs)

# initial solution
solution = Solution()
solution.populate(data.vehicles)
for job in data.jobs:
    nearest_vehicle = get_closest_vehicle(solution.routes, data.vehicles, data.matrix, job)
    route = [x for x in solution.routes if x.vehicle_id == nearest_vehicle.id][0]
    route.job_ids.append(job.id)
    route.load += job.delivery
for route in solution.routes:
    route.update_duration(data)
solution.update_duration()


# output
solution.export('output.json')

pass
