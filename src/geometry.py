import math
import random
from collections import deque

epsilon = 1e-12
def sgn(x):
    return (x > epsilon) - (x < -epsilon)

# ================================== 2d basis ==================================

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def len2(self):
        return self.x ** 2 + self.y ** 2
    def len(self):
        return math.sqrt(self.len2())
    def turn90(self): #anticlockwise
        return Point(-self.y, self.x)
    def norm(self):
        return Point(self.x / self.len(), self.y / self.len())
    def quad(self):
        return sgn(self.y) == 1 or (sgn(self.y) == 0 and sgn(self.x) >= 0)        
    def __str__(self):
        return "(%.3f, %.3f)" % (self.x, self.y)
    def __eq__(self, other):
        return (not sgn(self.x - other.x)) and (not sgn(self.y - other.y))
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    def scale(self, scalar):
        return Point(self.x * scalar, self.y * scalar)
    def __truediv__(self, scalar):
        return Point(self.x / scalar, self.y / scalar)
    def __xor__(self, other): #dot product
        return self.x * other.x + self.y * other.y
    def __mul__(self, other): #cross product
        return self.x * other.y - self.y * other.x
    def __lt__(self, other):
        if self.quad() != other.quad():
            return self.quad() < other.quad()
        else:
            return sgn((self * other)) > 0

class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def vec(self):
        return self.b - self.a
    def onLeft(self, p):
        return sgn((self.b - self.a) * (p - self.a)) > 0
    def __lt__(self, other):
        if sameDir(self, other):
            return other.onLeft(self.a)
        else:
            return (self.b - self.a) < (other.b - other.a)
    def __str__(self):
        return str(self.a) + "-" + str(self.b)

class Ball:
    def __init__(self, o, r):
        self.o = o
        self.r = r
    def getSplits(self, nsplits):
        gap = self.r * 2 / nsplits
        pos = [0.0]
        for i in range(nsplits):
            pos.append(pos[i] + gap)
        return pos

class Hypercube:
    def __init__(self, dim, bl, tr):
        self.dim = dim
        self.bl = bl
        self.tr = tr
        self.area = 1.0
        random.seed(2022)
        for i in range(self.dim):
            if sgn(tr[i] - bl[i]) <= 0:
                self.area = 0.0
                break
            else:
                self.area *= tr[i] - bl[i]
    def inside(self, hdp):
        for i in range(hdp.dim):
            if hdp.x[i] < self.bl[i] or hdp.x[i] > self.tr[i]:
                return False
        return True
    def sample(self, num):
        samples = []
        for i in range(num):
            x = []
            for j in range(self.dim):
                x.append(random.uniform(self.bl[j], self.tr[j]))
            samples.append(HDPoint(self.dim, x))
        return samples
    def intersectionAreaWithHypercube(self, hc):
        assert self.dim ==  hc.dim
        return hyperCubeIntersectionArea(self, hc)

class Hyperball:
    def __init__(self, dim, q, r, p):
        self.dim = dim
        self.q = q
        self.r = r
        self.p = p
        random.seed(2022)
        
        bl = []
        tr = []
        for i in range(self.dim):
            bl.append(q.x[i] - r)
            tr.append(q.x[i] + r)
        self._hc = Hypercube(dim, bl, tr)
        if self.dim == 2 and self.p == 2:
            self.area = math.pi * self.r * self.r
    def inside(self, hdp):
        assert self.dim == hdp.dim
        dist = 0.0
        for i in range(self.dim):
            dist += (hdp.x[i] - self.q.x[i]) ** self.p
        dist = math.pow(dist, 1 / self.p)
        if dist <= self.r:
            return True
        return False
    def getCircumscribedCube(self):
        return self._hc
    def sample(self, num):
        samples = []
        while len(samples) < num:
            hdp = self._hc.sample(1)[0]
            if self.inside(hdp):
                samples.append(hdp)
        return samples
    def toBall(self):
        assert self.dim == 2
        assert self.p == 2
        return Ball(Point(self.q.x[0], self.q.x[1]), self.r)
    def intersectionAreaWithHypercube(self, hc):
        assert self.dim == 2 and hc.dim == 2
        hc_corners = [Point(hc.bl[0], hc.bl[1]),
                      Point(hc.tr[0], hc.bl[1]),
                      Point(hc.tr[0], hc.tr[1]),
                      Point(hc.bl[0], hc.tr[1])]
        return ballPolygonIntersection(hc_corners, self.toBall())

class Hyperhalfspace:
    def __init__(self, dim, theta, b):
        self.dim = dim
        self.theta = theta
        self.b = b
        random.seed(2022)
        bl = [0.0] * dim
        tr = [1.0] * dim

        flag = True
        while flag:
            flag = False

            max_theta_x = []
            sum_max_theta_x = 0.0
            for i in range(dim):
                max_theta_x.append(max(bl[i] * theta[i], tr[i] * theta[i]))
                sum_max_theta_x += max_theta_x[i]
            for i in range(dim):
                if theta[i] == 0.0:
                    continue
                if theta[i] > 0.0:
                    lb = (b - (sum_max_theta_x - max_theta_x[i])) / abs(theta[i])
                    if lb > bl[i]:
                        bl[i] = lb
                        flag = True
                        break
                else:
                    ub = (-b + (sum_max_theta_x - max_theta_x[i])) / abs(theta[i])
                    if ub < tr[i]:
                        tr[i] = ub
                        flag = True
                        break

        self._hc = Hypercube(dim, bl, tr)

        if self.dim == 2:
            halfspaces = [Line(Point(0.0, 0.0), Point(1.0, 0.0)),
                          Line(Point(1.0, 0.0), Point(1.0, 1.0)),
                          Line(Point(1.0, 1.0), Point(0.0, 1.0)),
                          Line(Point(0.0, 1.0), Point(0.0, 0.0)),
                          self.toHalfspace()]
            self.area = convex_hull_area(halfSpaceIntersection(halfspaces))
    def inside(self, hdp):
        val = 0.0
        for i in range(self.dim):
            val += hdp.x[i] * self.theta[i]
        if sgn(val - self.b) >= 0:
            return True
        return False
    def sample(self, num):
        samples = []
        while len(samples) < num:
            hdp = self._hc.sample(1)[0]
            if self.inside(hdp):
                samples.append(hdp)
        return samples
    def toHalfspace(self):
        assert self.dim == 2
        if self.theta[1] == 0:
            p1 = Point(self.b / self.theta[0], 0.0)
            p2 = Point(self.b / self.theta[0], 1.0)
        else:
            p1 = Point(0.0, (self.b - self.theta[0] * 0.0) / self.theta[1])
            p2 = Point(1.0, (self.b - self.theta[0] * 1.0) / self.theta[1])
        corners = [Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)]
        for i in range(4):
            val = self.theta[0] * corners[i].x + self.theta[1] * corners[i].y
            if sgn(val - self.b) != 0:
                o = corners[i]
                if sgn((p1 - o) * (p2 - o)) * sgn(val - self.b) > 0:
                    return Line(p1, p2)
                else:
                    return Line(p2, p1)
        assert True
    def intersectionAreaWithHypercube(self, hc):
        assert self.dim == 2 and hc.dim == 2
        hc_corners = [Point(hc.bl[0], hc.bl[1]),
                      Point(hc.tr[0], hc.bl[1]),
                      Point(hc.tr[0], hc.tr[1]),
                      Point(hc.bl[0], hc.tr[1])]
        halfspaces = [Line(hc_corners[0], hc_corners[1]),
                      Line(hc_corners[1], hc_corners[2]),
                      Line(hc_corners[2], hc_corners[3]),
                      Line(hc_corners[3], hc_corners[0]),
                      self.toHalfspace()]
        return convex_hull_area(halfSpaceIntersection(halfspaces))

class HDPoint:
    def __init__(self, dim, x):
        self.dim = dim
        self.x = x

def det(a, b, c):
    return (b - a) * (c - a)

def parallel(l1, l2):
    return sgn(l1.vec() * l2.vec()) == 0

def intersect(l1, l2):
    s1 = det(l1.a, l1.b, l2.a)
    s2 = det(l1.a, l1.b, l2.b)
    return (l2.a.scale(s2) - l2.b.scale(s1)) / (s2 - s1)

def sameDir(l0, l1):
    return parallel(l0, l1) and sgn((l0.b - l0.a) ^ (l1.b - l1.a)) == 1

# ================================== half space intersection ==================================
def check(u, v, w):
    if parallel(u, v) and (not sameDir(u, v)):
        return False
    return w.onLeft(intersect(u, v))

# input : list of Line (the directed vectors must obey the rule of direction)
# output : list of Point of the convex hull (clockwise or anticlockwise)
def halfSpaceIntersection(l):
    l.sort()
    q = deque()
    for i in range(len(l)):
        if i > 0 and sameDir(l[i], l[i - 1]):
            continue
        while len(q) > 1 and (not check(q[len(q) - 2], q[len(q) - 1], l[i])):
            q.pop()
        while len(q) > 1 and (not check(q[1], q[0], l[i])):
            q.popleft()
        q.append(l[i])
    while len(q) > 2 and (not check(q[len(q) - 2], q[len(q) - 1], q[0])):
        q.pop()
    while len(q) > 2 and (not check(q[1], q[0], q[len(q) - 1])):
        q.popleft()
    if len(q) < 3:
        return []
    res = []
    for i in range(len(q)):
        res.append(intersect(q[i], q[(i + 1) % len(q)]))
    return res

# input : list of Point of a convex polygon (must be in order)
# output : area
def convex_hull_area(p):
    if len(p) <= 2:
        return 0.0
    area = 0.0
    for i in range(len(p) - 1):
        area += 0.5 * (p[i] * p[i + 1])
    area += 0.5 * (p[len(p) - 1] * p[0]) 
    return abs(area)

# input : list of Point of the convex hull
# output : all the halfspaces of the convex hull (anticlockwise and obey the rule of direction)
def getHalfSpaces(p):
    if len(p) <= 2:
        return []
    area = 0.0
    for i in range(len(p) - 1):
        area += 0.5 * (p[i] * p[i + 1])
    area += 0.5 * (p[len(p) - 1] * p[0]) 
    half_spaces = []
    if sgn(area) < 0:
        for i in range(len(p) - 1,0,-1):
            half_spaces.append(Line(p[i], p[i - 1]))
        half_spaces.append(Line(p[0], p[len(p) - 1]))
    else:
        for i in range(len(p) - 1):
            half_spaces.append(Line(p[i], p[i + 1]))
        half_spaces.append(Line(p[len(p) - 1], p[0]))
    return half_spaces

# ================================== ball polygon intersection ==================================
# input: two points that form a line, center, radius
# output: the list of intersection point(s) between the line and ball
def ballLineIntersection(a, b, ball):
    o, r = ball.o, ball.r
    p = []
    p1 = a - o
    d = b - a
    A = d ^ d
    B = 2 * (d ^ p1)
    C = (p1 ^ p1) - r ** 2

    delta = B ** 2 - 4 * A * C
    if sgn(delta) < 0: 
        return p # seperate
    if sgn(delta) == 0: # tangent
        t = -B / (2 * A)
        if sgn(t - 1) <= 0 and sgn(t) >= 0:
            p.append(a + d.scale(t))
        return p
    if sgn(delta) > 0: #intersect
        t1 = (-B - math.sqrt(delta)) / (2 * A)
        t2 = (-B + math.sqrt(delta)) / (2 * A)
        if sgn(t1 - 1) <= 0 and sgn(t1) >= 0:
            p.append(a + d.scale(t1))
        if sgn(t2 - 1) <= 0 and sgn(t2) >= 0:
            p.append(a + d.scale(t2))
        return p

def triangleArea(a, b):
    return 0.5 * abs(a * b)

def sectorArea(a, b, r):
    ang = math.atan2(a.y, a.x) - math.atan2(b.y, b.x)
    while ang <= 0:
        ang += 2 * math.pi
    while ang > 2 * math.pi:
        ang -= 2 * math.pi
    ang = min(ang, 2 * math.pi - ang)
    return r ** 2 * ang * 0.5

def calc(a, b, r):
    p = []
    if sgn(a.len() - r) < 0:
        if sgn(b.len() - r) < 0:
            return triangleArea(a, b)
        else:
            p = ballLineIntersection(a, b, Ball(Point(0.0, 0.0), r))
            return sectorArea(b, p[0], r) + triangleArea(a, p[0])
    else:
        p = ballLineIntersection(a, b, Ball(Point(0.0, 0.0), r))
        if sgn(b.len() - r) < 0:
            return sectorArea(a, p[0], r) + triangleArea(b, p[0])
        else:
            if len(p) == 2:
                return sectorArea(a, p[0], r) + sectorArea(b, p[1], r) + triangleArea(p[0], p[1])
            else:
                return sectorArea(a, b, r)


# input : point of a polygon (clockwise or anticlockwise), center of ball, radius 
# output : area
def ballPolygonIntersection(p, ball):
    area = 0.0
    np = len(p)
    for i in range(np):
        tmp = sgn((p[i] - ball.o) * (p[(i + 1) % np] - ball.o))
        if tmp != 0:
            area += tmp * calc(p[i] - ball.o, p[(i + 1) % np] - ball.o, ball.r)
    return abs(area)
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ High Dim @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ================================== hypercube intersection ==================================
# input : two hypercubes
# output : area of intersection of two hypercubes
def hyperCubeIntersectionArea(hc1, hc2):
    if hc1.dim != hc2.dim:
        return -1 # error
    res = 1.0
    for i in range(hc1.dim):
        bl = max(hc1.bl[i], hc2.bl[i])
        tr = min(hc1.tr[i], hc2.tr[i])
        if sgn(tr - bl) <= 0:
            return 0.0
        else:
            res *= tr - bl
    return res

# ================================== high-dim point in hypercube ==================================
# input : a hdpoint, a hypercube
# output : true/false
def hdPointInHypercube(hdp, hc):
    if hdp.dim != hc.dim:
        return False # error
    for i in range(hdp.dim):
        if hdp.x[i] < hc.bl[i] or hdp.x[i] > hc.tr[i]:
            return False
    return True

# test mode:
# halfSpaceIntersection : pass
# convex_hull_area : pass
# zero_halfSpace : fix and pass
# ball_polygon_area : pass
# precision : to be test

"""
if __name__ == "__main__":
    print(ballLineIntersection(Point(-0.248, -0.323), Point(-0.248, -0.315), Ball(Point(0.000, 0.000), 0.248)))

if __name__ == "__main__":
    p = [Point(1.0, -1.0), Point(2.0, 1.0), Point(2.0, 3.0), Point(1.0, 1.0)]
    o = Point(1.0, 1.0)
    r = 1.0
    ball = Ball(o, r)
    print(ballPolygonIntersection(p, ball))


if __name__ == "__main__":
    l = []
    # l.append(Line(Point(0.0, 0.0), Point(0.0, 2.0)))
    # l.append(Line(Point(2.0, 0.0), Point(0.0, 0.0)))
    # l.append(Line(Point(0.0, 1.0), Point(1.0, 1.0)))
    # l.append(Line(Point(1.0, 0.0), Point(3.0, 4.0)))
    # l.append(Line(Point(2.0, 0.0), Point(0.0, 2.0)))
    # l.append(Line(Point(0.0, 0.0), Point(0.0, 5.0)))
    # l.append(Line(Point(0.0, 0.0), Point(0.0, 3.0)))
    # l.append(Line(Point(0.0, 0.0), Point(0.0, 5.0)))
    # l.append(Line(Point(2.0, 0.0), Point(0.0, 2.0)))
    # l.append(Line(Point(3.0, 0.0), Point(0.0, 1.0)))
    # l.append(Line(Point(0.0, 5.0), Point(0.0, -1.0)))
    l.append(Line(Point(0.0, 0.0), Point(1.0, 0.0)))
    l.append(Line(Point(1.0, 0.0), Point(1.0, 1.0)))
    l.append(Line(Point(1.0, 1.0), Point(0.0, 1.0)))
    l.append(Line(Point(0.0, 1.0), Point(0.0, 0.0)))
    l.append(Line(Point(0.8, 1.0), Point(0.8, 0.0)))

    ps = halfSpaceIntersection(l)
    for i in range(len(ps)):
        print(ps[i])
    print(convex_hull_area(ps))
"""









