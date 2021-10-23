This is a solution to the algorithm challenge of instant delivery company.

- Problem is solved considering vehicle capacity constraints. 

- Since there are no time windows provided in the input data,
  service times of jobs become irrelevant for the routes, thus ignored.

- After generating an initial solution by assigning jobs to 
  their closest vehicle, route delivery durations are
  improved using local search operators.
  
- Using meta-heuristics algorithms may improve the solution quality,
  but skipped due to problem size.
  
- Program can be executed with "python your-current-path/main.py" command.

- Please see output.json for the results.

Ali Pala, 
alipala@buffalo.edu
