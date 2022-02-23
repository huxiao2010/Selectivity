### Yuxi
#### Problems:
* hdpoint_estimator is relatively slow for both ball queries and halfspace queries
* 99th and 100th q-errors of region_tree_estimator for forest-2d-ball is bad, where est_sel is pretty close to zero (about 1e-16, 1e-17, ...) while sel usually lies in [0.0001, 0.001) (0.006 also comes up once)
#### Todo list:
* [1] Implement region_tree_estimator for 2D ball query, 2D half-space query
* [1] Fix Isomer's bug that it only supports non-zero selectivity workload
* [1] Generate mixture testset
* [1] Implement mixture test for baseline, hdpoint, and region-tree
* [1] Implement hdpoint_estimator for high-dimensional ball query
* [1] Implement hdpoint_estimator for high-dimensional half-space query
* [1] Correct the calculation of q-error
* [1] Run hdpoint_estimator's experiments for Forest-4d/6d/8d/10d
* [1] Modify 'driver_'/'_estimator' for efficiency test
    - [1] rect
    - [1] region_tree
    - [1] hdpoint
* [1] Check java_impl_card_est for efficiency test
* [] Delete random seed in geometry.py
* [] Think about the necessity of adding 'similarity' in our paper (experiments)
* [] Read the manuscript
* [] Correct the input formatting of 'DMV/Instacart' for rect. query in 'xDMV/' and 'xInstacart'

#### Others :
* Implement all the codes in Java

#### Instructions used in experiments :
##### High-dimentional points estimator :
```bash
python driver_hdpoint.py --dataset Forest-2d --query_type rect --threshold 0.1 --alpha 0.1 --output_pre hdpoint/forest_2d_0.1_a0.1
python driver_hdpoint.py --dataset Forest-2d-data --query_type rect --threshold 0.1 --alpha 0.1 --output_pre hdpoint/new_forest_2d_0.1_a0.1
python driver_hdpoint.py --dataset Forest-2d --query_type rect --threshold 0.1 --alpha 0.0 --output_pre hdpoint/forest_2d_0.1_a0.0
python driver_hdpoint.py --dataset Forest-2d-data --query_type rect --threshold 0.1 --alpha 0.0 --output_pre hdpoint/new_forest_2d_0.1_a0.0
python driver_hdpoint.py --dataset Forest-2d --query_type rect --threshold 0.05 --alpha 0.1 --output_pre hdpoint/forest_2d_0.05_a0.1
python driver_hdpoint.py --dataset Forest-2d-data --query_type rect --threshold 0.05 --alpha 0.1 --output_pre hdpoint/new_forest_2d_0.05_a0.1
python driver_hdpoint.py --dataset Forest-2d --query_type rect --threshold 0.05 --alpha 0.0 --output_pre hdpoint/forest_2d_0.05_a0.0
python driver_hdpoint.py --dataset Forest-2d-data --query_type rect --threshold 0.05 --alpha 0.0 --output_pre hdpoint/new_forest_2d_0.05_a0.0
python driver_hdpoint.py --dataset Forest-2d --query_type rect --threshold 0.01 --alpha 0.1 --output_pre hdpoint/forest_2d_0.01_a0.1
python driver_hdpoint.py --dataset Forest-2d-data --query_type rect --threshold 0.01 --alpha 0.1 --output_pre hdpoint/new_forest_2d_0.01_a0.1
python driver_hdpoint.py --dataset Forest-2d --query_type rect --threshold 0.01 --alpha 0.0 --output_pre hdpoint/forest_2d_0.01_a0.0
python driver_hdpoint.py --dataset Forest-2d-data --query_type rect --threshold 0.01 --alpha 0.0 --output_pre hdpoint/new_forest_2d_0.01_a0.0
```

##### Efficiency test in Java :

rectangle_estimator(baseline) :
```bash
Modify train_size_array in driver_rect.py firstly (delete 1000, 2000)

[src/] python driver_rect.py --dataset Forest-2d --eff_test
[src/java_impl_card_est/] java card_est 2 rect_Forest-2d_tr50_te100 assertion_forest_2d
[src/java_impl_card_est/] java card_est 2 rect_Forest-2d_tr100_te100 assertion_forest_2d
[src/java_impl_card_est/] java card_est 2 rect_Forest-2d_tr200_te100 assertion_forest_2d
[src/java_impl_card_est/] java card_est 2 rect_Forest-2d_tr500_te100 assertion_forest_2d

[src/] python driver_rect.py --dataset Forest-2d-data --eff_test
[src/java_impl_card_est/] java card_est 2 rect_Forest-2d-data_tr50_te100 forest-data-2100-2d
[src/java_impl_card_est/] java card_est 2 rect_Forest-2d-data_tr100_te100 forest-data-2100-2d
[src/java_impl_card_est/] java card_est 2 rect_Forest-2d-data_tr200_te100 forest-data-2100-2d
[src/java_impl_card_est/] java card_est 2 rect_Forest-2d-data_tr500_te100 forest-data-2100-2d
```

region-tree estimator :
```bash
Add 2000 to train_size_array if necessary
Vary XXX in the instructions

[src/] python driver_region_tree.py --dataset Forest-2d-data --threshold 0.1 --eff_test
[src/java_impl_card_est/] java card_est 2 region-tree_Forest-2d-data_splXXX_bXXX_trXXX_teXXX forest-data-2100-2d
[src/] python driver_region_tree.py --dataset Forest-2d --threshold 0.1 --eff_test
[src/java_impl_card_est/] java card_est 2 region-tree_Forest-2d_splXXX_bXXX_trXXX_teXXX assertion_forest_2d
```

hdpoint estimator :
```bash
Vary XXX in the instructions
threshold = 0.100000/0.050000/0.010000
alpha = 0.000000/0.100000

[src/] python driver_hdpoint.py --dataset Forest-2d --query_type rect --threshold XXX --alpha XXX --eff_test
[src/java_impl_card_est/] java card_est XXX hdpoint_Forest-2d_splXXX_aXXX_trXXX_te100 assertion_forest_2d
[src/] python driver_hdpoint.py --dataset Forest-2d-data --query_type rect --threshold XXX --alpha XXX --eff_test
[src/java_impl_card_est/] java card_est XXX hdpoint_Forest-2d-data_splXXX_aXXX_trXXX_te100 forest-data-2100-2d
```

[baseline] ball estimator:
```bash
Please select appropriate training size
python driver_ball.py --dataset Forest-2d
```

[baseline] halfspace estimator:
```bash
Please select appropriate training size
python driver_halfspace.py --dataset Forest-2d --split poly
```

mixture dataset generator:
```bash
Code is /data/Mixture/mixer.py
python mixer.py --dataset Forest
python mixer.py --dataset Power
```

**[DEPRECATED]** driver_mixtest.py:
```bash
python driver_mixtest.py
Results are stored in ../results/Mixture/mixture_full.csv
```

region_tree_estimator for 2d halfspace query and 2d ball query:
```bash
It seems like threshold = 0.1 is enough for accuracy
python region_tree_estimator.py --dataset XXX --query_type halfspace --threshold XXX
python region_tree_estimator.py --dataset XXX --query_type ball --threhold XXX
```

mixture test:
```bash
python driver_mixture_test.py
```

### Haibo
#### dataset:
```bash
[data/workload/] and [data/workload/data_sensitive/] are for Quicksel and Isomer

[data/HighD]: For baseline, quad-tree and hd-pointd methods
1. assertion_NAME_'X'd.txt is random (old) workload
2. NAME-data-10000-'X'd.txt is data-sensitive workload
```
# Selectivity
