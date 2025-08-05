## Running Clojush Experiments

The `synthesize_gp.py` script is used to execute **Clojush** runs for the experiments.

###  Usage Instructions

#### For Training Set Size = 200

1. Open `synthesize_gp.py`.
2. In the `loop_through_tasks()` function, set the final argument (typically the number of training examples) to `200`.
3. To simulate 25 tasks with 100 runs each, call the function `25 * 100 = 2500` times.

#### For Training Set Size = 50

1. Again, modify the last argument of `loop_through_tasks()` to `50`.
2. For 25 tasks and 100 runs each, call the function `2500` times.

> Note: You can automate this by placing the function call inside a loop or by scripting the batch executions, depending on your compute environment.