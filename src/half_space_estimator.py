import time
import math
import numpy as np
from utility import calc_q_error
from geometry import convex_hull_area, halfSpaceIntersection, getHalfSpaces, intersect, parallel, Point, Line
from scipy.optimize import nnls

epsilon = 1e-5

def sgn(x):
    return (x > epsilon) - (x < -epsilon)
def sgn2(x, y):
    return sgn(x - y)

class HalfSpaceEstimator:
    def __init__(self, min_max, train_list):
        self.min_max = min_max
        self.train_list = train_list
        # each line is [a half-space (line), cardinality]

        self.n = len(train_list)
        self.dim = 2
        self._lines = [[], []]
        self._cnt = [0, 0]
        self._card = []
        self._train_error = 0.0
        self._buckets_half_spaces = []
        self._n_var = 0
        self._area = []
    def train(self, split):
        start_time = time.time()
        print("Number of queries : %d" % (self.n))

        if split == "rect":
            all_lines = self.min_max
            for i in range(len(self.train_list)):
                all_lines.append(self.train_list[i][0])
            all_points = []
            for i in range(len(all_lines)):
                for j in range(i + 1, len(all_lines)):
                    if not parallel(all_lines[i], all_lines[j]):
                        all_points.append(intersect(all_lines[i], all_lines[j]))
            ori_lines = [[0.0, 1.0], [0.0, 1.0]]
            for i in range(len(all_points)):
                ori_lines[0].append(all_points[i].x)
                ori_lines[1].append(all_points[i].y)
            for i in range(self.dim):
                ori_lines[i].sort()
                self._lines[i].append(ori_lines[i][0])
                for j in range(1, len(ori_lines[i])):
                    if sgn2(self._lines[i][len(self._lines[i]) - 1], ori_lines[i][j]) != 0:
                        self._lines[i].append(ori_lines[i][j])
                self._cnt[i] = len(self._lines[i]) - 1
            
            self._n_var = self._cnt[0] * self._cnt[1]
            print("Number of Variables: %d" % (self._n_var))
            self._area = []
            for i in range(self._cnt[0]):
                for j in range(self._cnt[1]):
                    x0, x1 = self._lines[0][i], self._lines[0][i + 1]
                    y0, y1 = self._lines[1][j], self._lines[1][j + 1]
                    self._area.append((x1 - x0) * (y1 - y0))
                    cur = []
                    cur.append(Line(Point(x0, y0), Point(x1, y0)))
                    cur.append(Line(Point(x1, y0), Point(x1, y1)))
                    cur.append(Line(Point(x1, y1), Point(x0, y1)))
                    cur.append(Line(Point(x0, y1), Point(x0, y0)))
                    self._buckets_half_spaces.append(cur)
            time_0 = time.time()
            print("Plane Split Time: %.3f" % (time_0 - start_time))
            
            A = []
            b = []
            for i in range(self.n):
                A.append([0.0] * self._n_var)
                for j in range(self._n_var):
                    convex_hull = halfSpaceIntersection([self.train_list[i][0]] + self._buckets_half_spaces[j])
                    hull_area = convex_hull_area(convex_hull)
                    A[i][j] = hull_area / self._area[j]
                b.append(self.train_list[i][1])
            A.append([1.0] * self._n_var)
            b.append(1.0)

            time_1 = time.time()
            print("Equation Construction Time : %.3f" % (time_1 - time_0))

            #currently, pure nnls
            A = np.array(A)
            b = np.array(b)
            x, self._train_error = nnls(A, b)
            time_2 = time.time()
            print("Equation Solving Time : %.3f" % (time_2 - time_1))

            for i in range(self._n_var):
                self._card.append(x[i])
            
            print("Training error : %.3f" % (self._train_error))
            return time.time() - start_time
        elif split == "poly":
            buckets = [[], [self.min_max]]
            area = [[], [1.0]]
            ii = 0 # in each iteration, we split buckets[1 - ii] and obtain buckets[ii]
            for i in range(self.n):
                a, b = self.train_list[i][0].a, self.train_list[i][0].b
                buckets[ii] = []
                area[ii] = []
                for j in range(len(buckets[1 - ii])):
                    cur_bucket = buckets[1 - ii][j]
                    sub_bucket_1 = halfSpaceIntersection(cur_bucket + [Line(a, b)])
                    sub_bucket_2 = halfSpaceIntersection(cur_bucket + [Line(b, a)])
                    area_1 = convex_hull_area(sub_bucket_1)
                    area_2 = convex_hull_area(sub_bucket_2)
                    if sgn(area_1) > 0 and sgn(area_2) > 0:
                        buckets[ii].append(getHalfSpaces(sub_bucket_1))
                        buckets[ii].append(getHalfSpaces(sub_bucket_2))
                        area[ii].append(area_1)
                        area[ii].append(area_2)
                    elif sgn(area_1) > 0 or sgn(area_2) > 0:
                        buckets[ii].append(cur_bucket)
                        area[ii].append(area[1 - ii][j])
                ii = 1 - ii
            self._buckets_half_spaces = buckets[1 - ii]
            self._area = area[1 - ii]
            self._n_var = len(self._buckets_half_spaces)

            time_0 = time.time()
            print("Number of Variables: %d" % (self._n_var))
            max_edges_of_bucket = 0
            for i in range(self._n_var):
                if len(self._buckets_half_spaces[i]) > max_edges_of_bucket:
                    max_edges_of_bucket = len(self._buckets_half_spaces[i])
            print("Maximal Number of Edges for All Buckets: %d" % (max_edges_of_bucket))
            print("Plane Split Time: %.3f" % (time_0 - start_time))
                        
            A = []
            b = []
            for i in range(self.n):
                A.append([0.0] * self._n_var)
                for j in range(self._n_var):
                    convex_hull = halfSpaceIntersection([self.train_list[i][0]] + self._buckets_half_spaces[j])
                    hull_area = convex_hull_area(convex_hull)
                    A[i][j] = hull_area / self._area[j]

                b.append(self.train_list[i][1])
            A.append([1.0] * self._n_var)
            b.append(1.0)

            time_1 = time.time()
            print("Equation Construction Time : %.3f" % (time_1 - time_0))

            #currently, pure nnls
            A = np.array(A)
            b = np.array(b)
            x, self._train_error = nnls(A, b)
            time_2 = time.time()
            print("Equation Solving Time : %.3f" % (time_2 - time_1))

            for i in range(self._n_var):
                self._card.append(x[i])
            
            print("Training error : %.3f" % (self._train_error))
            return time.time() - start_time, self._n_var

    def evaluate(self, test_list, pointers):
        start_time = time.time()
        error = 0.0
        test_len = len(test_list)
        est_result = []
        bad_test_count = 0

        for i in range(test_len):
            sel = test_list[i][1]
            est_sel = 0.0
            for j in range(self._n_var):
                area = self._area[j]
                d = self._card[j]
                convex_hull = halfSpaceIntersection([test_list[i][0]] + self._buckets_half_spaces[j])
                hull_area = convex_hull_area(convex_hull)
                est_sel += d / area * hull_area

            if est_sel >= 1.0 or est_sel <= 0.0:
                bad_test_count += 1
                est_sel = max(0.0 + epsilon, min(1.0 - epsilon, est_sel))

            error += (sel - est_sel) ** 2
            q_error = math.inf
            if est_sel == 0 or sel == 0:
                q_error = 1.000
            elif min(est_sel, sel) > 0:
                q_error = max(est_sel, sel) / min(est_sel, sel)
            est_result.append(q_error)
        
        rms = (error / test_len) ** 0.5
        ret_qerror = calc_q_error(est_result, pointers)
        return rms, ret_qerror, time.time() - start_time

