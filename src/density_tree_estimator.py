import math
import time
from tqdm import tqdm
import numpy as np
from scipy.optimize import nnls

from quad_tree import query_to_node
from utility import calc_q_error
from cvxopt import matrix, solvers, spdiag, log
from sklearn.linear_model import ElasticNet, Ridge, LinearRegression, Lasso

epsilon = 0.0001


class DensityTreeEstimator:
    def __init__(self, dimension, solver, train_list, test_list, tree):
        self.dimension = dimension
        self.solver = solver  # nnls

        # Bucket, Tree
        self.tree = tree
        self.buckets_list = tree.get_leaf_nodes()
        self.bucket_n = len(self.buckets_list)  # same as n_var

        # Train, Test
        self.train_list = train_list
        self.test_list = test_list
        self.train_n = len(train_list)
        self.test_n = len(test_list)
        self._train_error = 0.0

        # Qualified Queries
        self.threshold = 0.00001
        self._qualified_queries = []  # Filter low sel query (by threshold)
        self.q_n = 0

        # Results
        self._density = []

    def train(self, wkld_type):
        start_time = time.time()
        print("# of queries : %d" % self.train_n)
        A = []
        b = []

        if wkld_type == 'hs':
            print("Training for hs queries...")
            time_0 = time.time()
            for q in range(self.train_n):
                half_space_query = self.train_list[q]
                # query looks like [Line, sel]
                half_space_line = half_space_query[0]
                sel = half_space_query[1]

                # Find fraction with h-space in all the buckets
                fraction_list = self.tree.get_pointers_half_space(half_space_line, self.buckets_list)
                # print(half_space_line)
                # print(fraction_list)
                # input()
                A.append(fraction_list)
                b.append(sel)
        elif wkld_type == 'ball':
            print("Training for ball queries...")
            time_0 = time.time()
            for q in range(self.train_n):
                ball_query = self.train_list[q]
                # query looks like [ball, sel]
                ball = ball_query[0]
                sel = ball_query[1]

                # Find fraction with ball in all the buckets
                fraction_list = self.tree.get_pointers_ball(ball, self.buckets_list)
                if len(fraction_list) != self.bucket_n:
                    assert 'Wrong'
                A.append(fraction_list)
                b.append(sel)
        else:
            print("Training for rect queries...")
            for i in range(self.train_n):
                if self.train_list[i][2] >= self.threshold:
                    self._qualified_queries.append(self.train_list[i])
            self.q_n = len(self._qualified_queries)
            print("# of qualified queries : %d" % self.q_n)
            time_0 = time.time()
            print("=== Query Filter Time: %.3f(s)" % (time_0 - start_time))

            # Don't need plane split

            # Construct function
            for q in range(self.q_n):
                query = self._qualified_queries[q]
                # query looks like [[a, b], [c, d], sel]
                query_node = query_to_node(query[0] + query[1])
                # print("query", query_node)
                sel = query[2]

                # Find pointers to all the buckets having intersection
                involved_vars = self.tree.get_involved_pointers(query_node, self.buckets_list)
                # print(involved_vars)

                # Initialize A[][]
                A.append([0.0] * self.bucket_n)
                for i in range(len(involved_vars)):
                    pointer = involved_vars[i]
                    bucket = self.buckets_list[pointer]
                    # print(bucket)
                    area_inter = bucket.cal_intersects(query_node)
                    area_bucket = bucket.cal_area()
                    A[q][pointer] = (area_inter / area_bucket)
                b.append(sel)

        # Constrain: Sum of the sel == 1
        A.append([1.0] * self.bucket_n)
        b.append(1.0)

        # Solve function
        A = np.array(A)
        b = np.array(b)
        if self.solver == "nnls":
            # A = np.row_stack((A, np.array([0.001] * self.bucket_n)))
            # b = np.append(b, 0.0)
            x, self._train_error = nnls(A, b)
            # print("ABX: ", A, b, x)
        else:
            x = []
            self._train_error = math.inf

        time_1 = time.time()
        print("=== Equation Construction and Solving Time: %.3f(s)" % (time_1 - time_0))

        layers = {} # layer_hash -> [total_density, total_area / size]
        for i in range(self.bucket_n):
            val = hash(tuple(A[:, i]))
            if val not in layers:
                layers[val] = [0.0, 0.0]
            layers[val][0] += x[i]
            layers[val][1] += self.buckets_list[i].cal_area()
            # layers[val][1] += 1.0
        for i in range(self.bucket_n):
            val = hash(tuple(A[:, i]))
            self._density.append(layers[val][0] / layers[val][1] * self.buckets_list[i].cal_area())
            # self._density.append(layers[val][0] / layers[val][1])
            # self._density.append(x[i])
        time_2 = time.time()
        print("=== Reassignment Time: %.3f(s)" % (time_2 - time_1))

        print("Training error: %.3f" % self._train_error)
        end_time = time.time()

        count = 0
        for i in self._density:
            if i <= 0.0:
                count += 1
            # else:
            #     print(i)
        print("<= Zero Area: ", count, len(self._density), count / len(self._density))

        return end_time - time_0

    def evaluate(self, error_pointers, by_density, wkld_type):
        raw_data_n = self.tree.cal_val()
        error = 0.0
        test_n = len(self.test_list)
        est_result = []
        bad_test_count = 0
        large_q_error_count = 0
        total_time = 0

        print("Sum = ", sum(self._density))

        for q in range(test_n):
            est_sel = 0.0
            start_time = time.time()
            test_query = self.test_list[q]

            if wkld_type == 'hs':
                # query looks like [Line, sel]
                half_space_line = test_query[0]
                sel = test_query[1]

                fraction_list = self.tree.get_pointers_half_space(half_space_line, self.buckets_list)
                if len(fraction_list) != self.bucket_n:
                    assert "ERROR"

                for i in range(len(fraction_list)):
                    est_sel += fraction_list[i] * self._density[i]
            elif wkld_type == 'ball':
                # query looks like [ball, sel]
                ball = test_query[0]
                sel = test_query[1]

                fraction_list = self.tree.get_pointers_ball(ball, self.buckets_list)
                for i in range(len(fraction_list)):
                    est_sel += fraction_list[i] * self._density[i]
            else:
                sel = test_query[2]
                query_node = query_to_node(test_query[0] + test_query[1])
                est_sel = 0.0
                buckets_list = self.buckets_list

                involved_vars = self.tree.get_involved_pointers(query_node, buckets_list)

                for p in range(len(involved_vars)):
                    pointer = involved_vars[p]
                    bucket = self.buckets_list[pointer]
                    area_inter = bucket.cal_intersects(query_node)
                    area_bucket = bucket.cal_area()
                    if by_density:
                        # est_sel += area_inter / area_bucket * (len(bucket.points_in_leaf) / raw_data_n)
                        est_sel += area_inter / area_bucket * bucket.sel
                    else:
                        est_sel += area_inter / area_bucket * self._density[pointer]

            if est_sel > 1.0 or est_sel < 0.0001:
                bad_test_count += 1
                est_sel = max(0.0 + epsilon, min(1.0 - epsilon, est_sel))

            total_time += time.time() - start_time

            # print(sel, est_sel)
            error += (sel - est_sel) ** 2
            # if abs(sel - est_sel) > 0.005:
            #     print("diff > 0.005: ", sel, est_sel)

            if min(est_sel, sel) == 0:
                if abs(est_sel - sel) <= 0.0001:
                    q_error = 1
                else:
                    q_error = max(est_sel, sel) / 0.0001
            else:
                q_error = max(est_sel, sel) / min(est_sel, sel)
            if q_error > 5:
                large_q_error_count += 1
                # print(q_error, est_sel, sel)
            est_result.append(q_error)

        print('Estimation Done...')
        print('=== Estimation Time : %.3f(s)' % (total_time / test_n))
        print("# of Bad Test: ", bad_test_count)
        print("# of large q_error (>5): ", large_q_error_count)

        rms = (error / test_n) ** 0.5
        ret_qerror = calc_q_error(est_result, error_pointers)
        return rms, ret_qerror, round(total_time / test_n, 3)

