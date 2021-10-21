import time
from data import read
from data.model import Solution, Route
from helpers import *
from local_search import *

if __name__ == "__main__":

    # start of algorithm
    start_time = time.time()

    # reading data
    data = read.data

    # generate initial solution
    solution = Solution('Instant Delivery')
    solution = generate_initial_solution(data, solution)

    # improve routes with local search
    solution = local_search(data, solution)

    # export solution
    solution.export('output.json')

    # end of algorithm
    print("{0} solution prepared in {1:.3f} seconds.".format(
          solution.name, (time.time() - start_time)))
