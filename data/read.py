import json
from data.paths import FILE_PATH, FILE_NAME
from data.model import Data, Vehicle, Job


data = Data()

with open(FILE_PATH + FILE_NAME) as json_file:
    row_data = json.load(json_file)

for item in row_data['vehicles']:
    data.vehicles.append(Vehicle(item['id'], item['start_index'], item['capacity'][0]))

for item in row_data['jobs']:
    data.jobs.append(Job(item['id'], item['location_index'], item['delivery'][0], item['service']))

for item in row_data['matrix']:
    data.matrix.append(item)
