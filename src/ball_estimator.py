import time
import math
import numpy as np
from utility import calc_q_error, sgn2
from geometry import Point, ballPolygonIntersection, Ball
from scipy.optimize import nnls

epsilon = 0.001

class BallEstimator:
    def __init__(self, min_max, train_list):
        self.min_max = min_max
        self.train_list = train_list
        # each line is [ball, cardinality]

        self.n = len(train_list)
        self.dim = 2
        self._lines = [[], []]
        self._cnt = [0, 0]
        self._card = []
        self._train_error = 0.0
        self._n_var = 0
        self._area = []
        self._corners = []
    def train(self, nsplits):
        start_time = time.time()
        print("Number of queries : %d" % (self.n))

        all_lines = [[self.min_max[0][0], self.min_max[1][0]], [self.min_max[0][1], self.min_max[1][1]]]
        for i in range(len(self.train_list)):
            ball = self.train_list[i][0]
            pos = ball.getSplits(nsplits)
            for j in range(self.dim):
                all_lines[j].extend(pos)
        
        for i in range(self.dim):
            all_lines[i].sort()

            self._lines[i].append(all_lines[i][0])
            self._cnt[i] = 1
            for j in range(1, len(all_lines[i])):
                if sgn2(self._lines[i][self._cnt[i] - 1], all_lines[i][j]) != 0:
                    self._lines[i].append(all_lines[i][j])
                    self._cnt[i] += 1
            self._cnt[i] -= 1
    
        self._n_var = self._cnt[0] * self._cnt[1]
        print("Number of Variables: %d" % (self._n_var))
        self._area = []
        self._corners = []
        for i in range(self._cnt[0]):
            for j in range(self._cnt[1]):
                x0, x1 = self._lines[0][i], self._lines[0][i + 1]
                y0, y1 = self._lines[1][j], self._lines[1][j + 1]
                self._area.append((x1 - x0) * (y1 - y0))
                self._corners.append([Point(x0, y0), Point(x1, y0), Point(x1, y1), Point(x0, y1)])

        time_0 = time.time()
        print("Plane Split Time: %.3f" % (time_0 - start_time))
            
        A = []
        b = []
        for i in range(self.n):
            A.append([0.0] * self._n_var)
            for j in range(self._n_var):
                int_area = ballPolygonIntersection(self._corners[j], Ball(self.train_list[i][0].o, self.train_list[i][0].r))
                A[i][j] = int_area / self._area[j]
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
                int_area = ballPolygonIntersection(self._corners[j], test_list[i][0])
                est_sel += d / area * int_area

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

