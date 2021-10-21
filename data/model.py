from helpers import *
import pandas as pd
import json


class Data:
    vehicles = []
    jobs = []
    matrix = []


class Vehicle:
    def __init__(self, id, start_index, capacity):
        self.id = id
        self.start_index = start_index
        self.capacity = capacity


class Job:
    def __init__(self, id, location_index, delivery, service):
        self.id = id
        self.location_index = location_index
        self.delivery = delivery
        self.service = service


class Route:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.job_ids = []
        self.delivery_duration = 0
        self.load = 0

    def update_duration(self, data):
        start_index = [x for x in data.vehicles if x.id == self.vehicle_id][0].start_index
        location_indices = [start_index]
        for job_id in self.job_ids:
            job = [v for v in data.jobs if v.id == job_id][0]
            location_indices.append(job.location_index)
        self.delivery_duration = route_distance(data.matrix, location_indices)

    def copy(self):
        copy = Route(self.vehicle_id)
        copy.delivery_duration = self.delivery_duration
        copy.load = self.load
        job_ids = []
        for job_id in self.job_ids:
            job_ids.append(job_id)
        copy.job_ids = job_ids
        return copy


class Solution:
    def __init__(self):
        self.total_delivery_duration = 0
        self.routes = []

    def populate(self, vehicles):
        for vehicle in vehicles:
            self.routes.append(Route(vehicle.id))

    def update_duration(self):
        duration = 0
        for route in self.routes:
            duration += route.delivery_duration
        self.total_delivery_duration = duration

    def export(self, path):
        to_json = json.dumps(self, default=lambda o: o.__dict__)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(json.loads(to_json), f, ensure_ascii=False, indent=4)
