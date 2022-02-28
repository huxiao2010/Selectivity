# Selectivity Functions of Range Queries are Learnable

## Project Structure

In `/src`,

1. `hdpoint` is correponding to __PtsHist__, while `region_tree` is for __QuadHist__.
1. `driver_*.py` are the drivers for experiments, with different input parameters.
1. `*_estimator.py` are the estimators, with `train()` and `evaluate()` as interfaces for their drivers.
1. `utility.py` includes various data loaders, error metrics, and other shared tools for the estimators.
1. `geometry.py` includes some geometric computations, like rectangle intersection.

## Important Pieces

We present the pseudo-codes of our algorithms' frameworks in the following.  

### driver_*

```
load_data()
estimator = build_estimator()
estimator.train()
estimator.evaluate()
get_results()
```

### region_tree_estimator (QuadHist)

```
class RegionTreeEstimator:
	...
	def train():
		tree = build_region_tree()
		for train_data in train_list:
			recursively_split(tree, train_data)

		build_equation_system()
		solve()

	def evaluate():
		for test_data in test_list:
			calc(test_data)
	...

```

### hdpoint_estimator (PtsHist)

```
class HDPointEstimator:
	...
	def train():
		weighted_points = []
		for train_data in train_list:
			weighted_points.append(train_data.sample())

		build_equation_system()
		solve()

	def evaluate():
		for test_data in test_list:
			calc(test_data)
	...

```

## Instructions

```
# driver_region_tree.py
# Vary XXX in the instruction, or use '--help' for hints
python driver_region_tree.py --dataset XXX --query_type XXX --train_size XXX --threshold XXX --buckets_limit XXX --test_size XXX --solver XXX
```

```
# driver_hdpoint.py
# Vary XXX in the instruction, or use '--help' for hints
python driver_hdpoint.py --dataset XXX --query_type XXX --train_size XXX --threshold XXX --buckets_limit XXX --alpha XXX --test_size XXX
```

To test other workloads, firstly add path and filename for both workload and min_max_range for data loaders in `utility.py`, place them in the corresponding position, and then add the new item into `--dataset []`. We will give more concrete examples in the released version.


## Special Packages Requirement
```
scipy >= 1.7.2
cvxopt >= 1.2.7 (if use)
cplex >= 20.1.0.1 (and a license, if use)
gurobipy >= 9.5.0 (and a license, if use)
```

## Example: Some Figures' Configuration
### Figure 9
```
trainsize_buckets_threshold = {
	50 : [
		[100, 0.052],
		[500, 0.012],
		[1000, 0.0061],
		[5000, 0.0015],
		[10000, 0.0007]
	],
	200 : [
		[100, 0.08],
		[500, 0.018],
		[1000, 0.0096],
		[5000, 0.0021],
		[10000, 0.0013]
	],
	500 : [
		[100, 0.08],
		[500, 0.0205],
		[1000, 0.011],
		[5000, 0.00267],
		[10000, 0.0014]
	],
	1000 : [
		[100, 0.11],
		[500, 0.025],
		[1000, 0.014],
		[5000, 0.003],
		[10000, 0.0017]
	],
	2000 : [
		[100, 0.125],
		[500, 0.03],
		[1000, 0.016],
		[5000, 0.0033],
		[10000, 0.0019]
	]
}
```
Use triple (train_size, buckets_limit, threshold) as above in the following instruction
```
python3 drive_region_tree.py --dataset Power-2d-data --query_type rect --train_size XXX --threshold XXX --buckets_limit XXX --test_size 100 --solver nnls 
```

### Figure 27, 28, 26
```
trainsize_buckets_threshold = {
    50 : [
        [100, 0.052],
        [500, 0.0105],
        [1000, 0.0063],
        [5000, 0.0015],
        [10000, 0.0006],
        [50000, 0.00015],
        [100000, 0.00007]
    ],
    200 : [
        [100, 0.08],
        [500, 0.018],
        [1000, 0.0096],
        [5000, 0.0021],
        [10000, 0.001],
        [50000, 0.0002],
        [100000, 0.0001]
    ],
    500 : [
        [100, 0.08],
        [500, 0.02],
        [1000, 0.0105],
        [5000, 0.0025],
        [10000, 0.0014],
        [50000, 0.0003],
        [100000, 0.00015]
    ],
    1000 : [
        [100, 0.11],
        [500, 0.027],
        [1000, 0.015],
        [5000, 0.0031],
        [10000, 0.0016],
        [50000, 0.0004],
        [100000, 0.00016]
    ],
    2000 : [
        [100, 0.125],
        [500, 0.031],
        [1000, 0.016],
        [5000, 0.0036],
        [10000, 0.0019],
        [50000, 0.0004],
        [100000, 0.0002]
    ]
}
```
Use triple(train_size, buckets_limit, threshold) as above in the following instruction
```
python3 driver_region_tree.py --dataset Power-2d-data --query_type rect --train_size XXX --buckets_limit XXX --threshold XXX --test_size 1000 --solver gurobi_linf
```
