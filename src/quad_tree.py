import numpy as np
import random
from tqdm import tqdm
import matplotlib.pyplot as plt
from utility import rectangle_intersection
from geometry import getHalfSpaces, Point, Line, halfSpaceIntersection, convex_hull_area, ballPolygonIntersection, Ball

threshold = 40
sel_threshold = 0.01
undividable_n = 0

class TreePoint:
    """A point located at (x,y) in 2D space."""
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return 'P({:.2f}, {:.2f})'.format(self.x, self.y)

    def distance_to(self, other):
        try:
            other_x, other_y = other.x, other.y
        except AttributeError:
            other_x, other_y = other
        return np.hypot(self.x - other_x, self.y - other_y)

class TreeNode:
    """A rectangle(Node) centred at (cx, cy) with width w and height h."""
    def __init__(self, cx, cy, w, h, is_leaf):
        self.is_leaf = is_leaf
        self.cx, self.cy = cx, cy
        self.w, self.h = w, h
        self.west_edge, self.east_edge = cx - w / 2, cx + w / 2
        self.north_edge, self.south_edge = cy - h / 2, cy + h / 2
        self.points_in_leaf = []
        self.sel = 0.0
        self.undividable = False # label for those nodes with very low (0) sel, don't divide them

    def __str__(self):
        return '({:.2f}, {:.2f}, {:.2f}, {:.2f})'.format(self.west_edge,
                                                         self.north_edge, self.east_edge, self.south_edge)

    def contains(self, point):
        """Is point (a Point object or (x,y) tuple) inside this Node(Rect)?"""
        try:
            point_x, point_y = point.x, point.y
        except AttributeError:
            point_x, point_y = point

        return (self.west_edge <= point_x < self.east_edge and
                self.north_edge <= point_y < self.south_edge)

    def count_contains(self, point_list):
        """Count how many Point inside this Node(Rect)"""
        count = 0
        for i in point_list:
            if self.contains(i):
                count += 1
        self.val = self.count_contains(point_list=point_list)
        return count

    def draw(self, ax, alpha, c='k', lw=0.02, **kwargs, ):
        x1, y1 = self.west_edge, self.north_edge
        x2, y2 = self.east_edge, self.south_edge
        if alpha < 0.01:
            ax.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], c='#808080', lw=lw, alpha=1, **kwargs)
        else:
            # ax.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], c=c, lw=lw, alpha=1, **kwargs)
            ax.fill([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1], c=c, lw=lw, alpha=alpha, **kwargs)

    def draw_old(self, ax, c='b', lw=1, **kwargs):
        x1, y1 = self.west_edge, self.north_edge
        x2, y2 = self.east_edge, self.south_edge
        ax.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], c=c, lw=lw, **kwargs)

    def is_intersects(self, other):
        """Does Rect object other intersect this Rect?"""
        return not (other.west_edge > self.east_edge or
                    other.east_edge < self.west_edge or
                    other.north_edge > self.south_edge or
                    other.south_edge < self.north_edge)

    def cal_area(self):
        area = self.w * self.h
        return area

    def cal_intersects(self, other):
        """What is the area of the two rects"""
        rect1 = [[self.cx - self.w / 2, self.cy - self.h / 2], [self.cx + self.w / 2, self.cy + self.h / 2]]
        rect2 = [[other.cx - other.w / 2, other.cy - other.h / 2], [other.cx + other.w / 2, other.cy + other.h / 2]]
        return rectangle_intersection(rect1, rect2)


class DensityTree:
    """A class implementing a quadtree."""
    def __init__(self, root, max_sons=threshold, depth=0):
        self.root = root
        self.max_sons = max_sons
        self.depth = depth

        self.points = []
        self.outside_points_num = 0

    def split(self):
        """Split the large node to 4 equal small nodes"""
        cx, cy = self.root.cx, self.root.cy
        w, h = self.root.w, self.root.h
        self.north_west = DensityTree(TreeNode(cx - w / 4, cy + h / 4, w / 2, h / 2, True), self.max_sons, self.depth + 1)
        self.north_east = DensityTree(TreeNode(cx + w / 4, cy + h / 4, w / 2, h / 2, True), self.max_sons, self.depth + 1)
        self.south_west = DensityTree(TreeNode(cx - w / 4, cy - h / 4, w / 2, h / 2, True), self.max_sons, self.depth + 1)
        self.south_east = DensityTree(TreeNode(cx + w / 4, cy - h / 4, w / 2, h / 2, True), self.max_sons, self.depth + 1)
        self.root.is_leaf = False

    def split_by_query(self, query_node):
        """Split the large node to 4 small nodes, the central is corner of query"""
        x1 = self.root.cx - self.root.w / 2
        x2 = self.root.cx + self.root.w / 2
        y1 = self.root.cy + self.root.h / 2
        y2 = self.root.cy - self.root.h / 2
        query_x1 = query_node.cx - query_node.w / 2
        query_x2 = query_node.cx + query_node.w / 2
        query_y1 = query_node.cy + query_node.h / 2
        query_y2 = query_node.cy - query_node.h / 2
        inside_x = 0
        inside_y = 0
        if x1 < query_x1 < x2:
            inside_x = query_x1
            if y1 < query_y1 < y2:
                inside_y = query_y1
            elif y1 < query_y2 < y2:
                inside_y = query_y2
        elif x1 < query_x2 < x2:
            inside_x = query_x2
            if y1 < query_y1 < y2:
                inside_y = query_y1
            elif y1 < query_y2 < y2:
                inside_y = query_y2
        if inside_x != 0 or inside_y != 0:
            self.north_west = DensityTree(
                TreeNode(x1 + (inside_x - x1) / 2, y2 - (y2 - inside_y) / 2, inside_x - x1, y2 - inside_y, True),
                self.max_sons,
                self.depth + 1)
            self.north_east = DensityTree(
                TreeNode(x2 - (x2 - inside_x) / 2, y2 - (y2 - inside_y) / 2, x2 - inside_x, y2 - inside_y, True),
                self.max_sons,
                self.depth + 1)
            self.south_west = DensityTree(
                TreeNode(x1 + (inside_x - x1) / 2, y1 + (inside_y - y1) / 2, inside_x - x1, inside_y - y1, True),
                self.max_sons,
                self.depth + 1)
            self.south_east = DensityTree(
                TreeNode(x2 - (x2 - inside_x) / 2, y1 + (inside_y - y1) / 2, x2 - inside_x, inside_y - y1, True),
                self.max_sons,
                self.depth + 1)
            self.root.is_leaf = False

    def insert(self, point):
        """Try to insert point into this QuadTree."""
        if not self.root.contains(point):
            # The point does not lie inside boundary: bail.
            if self.depth == 0:
                self.outside_points_num += 1
            return False
        if self.root.is_leaf and len(self.points) < self.max_sons:
            # There's room for our point without dividing the QuadTree.
            self.points.append(point)
            # print("depth:", self.depth, "count: ", len(self.points))
            self.root.points_in_leaf.append(point)
            return True

        # No room: divide if necessary, then try the sub-quads.
        if self.root.is_leaf:
            self.split()
            for point_i in self.points:
                self.north_east.insert(point_i)
                self.north_west.insert(point_i)
                self.south_west.insert(point_i)
                self.south_east.insert(point_i)
            self.points = []

        return (self.north_east.insert(point) or
                self.north_west.insert(point) or
                self.south_east.insert(point) or
                self.south_west.insert(point))

    def insert_by_query(self, query, thres):
        query_node = query_to_node(query[0]+query[1])
        if self.root.is_leaf:
            inter_area = self.root.cal_intersects(query_node)
            leaf_node_area = self.root.cal_area()
            if inter_area > 0:
                covered_sel = query[2] / query_node.cal_area() * inter_area
                if covered_sel > thres:
                    # self.split_by_query(query_node)
                    self.split()
                    self.north_east.insert_by_query(query, thres)
                    self.north_west.insert_by_query(query, thres)
                    self.south_west.insert_by_query(query, thres)
                    self.south_east.insert_by_query(query, thres)
                else:
                    self.root.sel = covered_sel
                    return True
        else:
            self.north_east.insert_by_query(query, thres)
            self.north_west.insert_by_query(query, thres)
            self.south_east.insert_by_query(query, thres)
            self.south_west.insert_by_query(query, thres)

    def insert_by_half_space(self, hf, sel, plane):
        if self.root.undividable:
            return
        if self.root.is_leaf:
            cur_quad_tree_node = self.root
            rect_spaces = quad_tree_node_to_half_space(cur_quad_tree_node)

            sub_bucket_1 = halfSpaceIntersection([hf] + rect_spaces)
            area_1 = convex_hull_area(sub_bucket_1)

            # if area_1 > 0 or area_2 > 0:
            if area_1 > 0 :
                # one half space will divide 1*1 plane to 2 spaces
                half_space_area_with_plane_1 = halfSpaceIntersection([hf] + plane)
                area_with_plane_1 = convex_hull_area(half_space_area_with_plane_1)
                if area_with_plane_1 == 0:
                    return True  # TODO: check it

                covered_sel_1 = sel / area_with_plane_1 * area_1

                if covered_sel_1 > sel_threshold:
                    self.split()
                    # print("Split")
                    self.north_east.insert_by_half_space(hf, sel, plane)
                    self.north_west.insert_by_half_space(hf, sel, plane)
                    self.south_west.insert_by_half_space(hf, sel, plane)
                    self.south_east.insert_by_half_space(hf, sel, plane)
                else:
                    self.root.sel = covered_sel_1
                    return True
        else:
            self.north_east.insert_by_half_space(hf, sel, plane)
            self.north_west.insert_by_half_space(hf, sel, plane)
            self.south_west.insert_by_half_space(hf, sel, plane)
            self.south_east.insert_by_half_space(hf, sel, plane)
            return True

    def insert_by_ball(self, ball, sel, plane):
        if self.root.undividable:
            return
        if self.root.is_leaf:
            cur_quad_tree_node = self.root
            corners = quad_tree_node_to_points(cur_quad_tree_node)
            inter_area = ballPolygonIntersection(corners, ball)
            if inter_area > 0:
                ball_area = pow(ball.r, 2) * 3.141
                ball_in_plane_area = ballPolygonIntersection(plane, ball)
                covered_sel = sel * inter_area / ball_in_plane_area
                if covered_sel > sel_threshold:
                    self.split()
                    # print("split")
                    self.north_east.insert_by_ball(ball, sel, plane)
                    self.north_west.insert_by_ball(ball, sel, plane)
                    self.south_west.insert_by_ball(ball, sel, plane)
                    self.south_east.insert_by_ball(ball, sel, plane)
                else:
                    # print(covered_sel, sel, inter_area, ball_area)
                    # input()
                    self.root.sel = covered_sel
                    return True
        else:
            return (self.north_east.insert_by_ball(ball, sel, plane) or
                    self.north_west.insert_by_ball(ball, sel, plane) or
                    self.south_east.insert_by_ball(ball, sel, plane) or
                    self.south_west.insert_by_ball(ball, sel, plane))

    def pre_assign_by_hf(self, hf, sel, plane):
        """The area covered by this hf can not be divided in the future"""
        global undividable_n
        if self.root.undividable:
            return
        if self.root.is_leaf:
            cur_quad_tree_node = self.root
            rect_spaces = quad_tree_node_to_half_space(cur_quad_tree_node)
            sub_bucket = halfSpaceIntersection([hf] + rect_spaces)
            inter_area = convex_hull_area(sub_bucket)
            rect_area = cur_quad_tree_node.cal_area()

            if inter_area == rect_area:
                # The node is totally covered by the hf
                self.root.undividable = True
                half_space_area_with_plane = halfSpaceIntersection([hf] + plane)
                area_with_plane = convex_hull_area(half_space_area_with_plane)
                self.root.sel = sel / area_with_plane * inter_area
                undividable_n += 1
            else:
                return
        else:
            return (self.north_east.pre_assign_by_hf(hf, sel, plane) or
                    self.north_west.pre_assign_by_hf(hf, sel, plane) or
                    self.south_east.pre_assign_by_hf(hf, sel, plane) or
                    self.south_west.pre_assign_by_hf(hf, sel, plane))

    def pre_assign_by_ball(self, ball, sel, plane):
        """The area covered by this ball can not be divided in the future"""
        global undividable_n
        if self.root.undividable:
            return
        if self.root.is_leaf:
            cur_quad_tree_node = self.root
            corners = quad_tree_node_to_points(cur_quad_tree_node)
            node_area = cur_quad_tree_node.cal_area()
            inter_area = ballPolygonIntersection(corners, ball)
            if inter_area == node_area:
                # The node is totally covered by the ball
                self.root.undividable = True
                ball_in_plane_area = ballPolygonIntersection(plane, ball)
                self.root.sel = sel * inter_area / ball_in_plane_area
                # print("Find a undividable", str(cur_quad_tree_node), ball.o.x, ball.o.y, ball.r)
                undividable_n += 1
            else:
                return
        else:
            return (self.north_east.pre_assign_by_ball(ball, sel, plane) or
                    self.north_west.pre_assign_by_ball(ball, sel, plane) or
                    self.south_east.pre_assign_by_ball(ball, sel, plane) or
                    self.south_west.pre_assign_by_ball(ball, sel, plane))

    def cal_val(self):
        """How many points in the tree"""
        if self.root.is_leaf:
            # print("is leaf")
            count = len(self.points)
            # print(count)
        else:
            count = len(self.points) + self.north_east.cal_val() + self.north_west.cal_val() \
                    + self.south_west.cal_val() + self.south_east.cal_val()
        return count

    def cal_nodes(self):
        if self.root.is_leaf:
            return 1
        else:
            return self.north_east.cal_nodes() + self.north_west.cal_nodes() +\
                   self.south_west.cal_nodes() + self.south_east.cal_nodes()

    def cal_depth(self):
        if self.root.is_leaf:
            return 1
        else:
            depth_nw = self.north_west.cal_depth()
            depth_ne = self.north_east.cal_depth()
            depth_sw = self.south_west.cal_depth()
            depth_se = self.south_east.cal_depth()
            tmp_list = [depth_nw, depth_ne, depth_se, depth_sw]
            return max(tmp_list) + 1

    def get_leaf_nodes(self):
        """Return a list of all the leaf nodes"""
        # dfs
        leaf_nodes_list = []
        if self.root.is_leaf:
            leaf_nodes_list.append(self.root)
        else:
            list_nw = self.north_west.get_leaf_nodes()
            list_ne = self.north_east.get_leaf_nodes()
            list_sw = self.south_west.get_leaf_nodes()
            list_se = self.south_east.get_leaf_nodes()
            leaf_nodes_list = list_nw + list_ne + list_sw + list_se
        return leaf_nodes_list

    @staticmethod
    def get_involved_pointers(query, leaf_nodes_list):
        """Return all nodes that intersect with query"""
        involved_pointers = []
        for i in range(len(leaf_nodes_list)):
            if query.is_intersects(leaf_nodes_list[i]):
                involved_pointers.append(i)
        return involved_pointers

    @staticmethod
    def get_pointers_half_space(half_space_query, leaf_nodes_list):
        """Return fraction list of node that intersect with query in one half space, 0 or a/b """
        pointers = []
        for i in range(len(leaf_nodes_list)):
            leaf_node_half_spaces = quad_tree_node_to_half_space(leaf_nodes_list[i])
            covered = halfSpaceIntersection([half_space_query] + leaf_node_half_spaces)
            covered_area = convex_hull_area(covered)
            if covered_area > 0:
                leaf_node_area = leaf_nodes_list[i].cal_area()
                pointers.append(covered_area / leaf_node_area)
            else:
                pointers.append(0)
        return pointers

    @staticmethod
    def get_pointers_ball(ball, leaf_nodes_list):
        pointers = []
        for i in range(len(leaf_nodes_list)):
            leaf_node = quad_tree_node_to_points(leaf_nodes_list[i])
            covered_area = ballPolygonIntersection(leaf_node, ball)
            if covered_area > 0:
                leaf_node_area = leaf_nodes_list[i].cal_area()
                pointers.append(covered_area / leaf_node_area)
            else:
                pointers.append(0)
        return pointers

    def draw(self, ax):
        """Draw a representation of the quadtree on Matplotlib Axes ax."""
        self.root.draw_old(ax)
        if not self.root.is_leaf:
            self.north_west.draw(ax)
            self.north_east.draw(ax)
            self.south_east.draw(ax)
            self.south_west.draw(ax)


def build_quad_tree_by_points(points):
    print("Build quad tree by sampled nodes...")
    root = TreeNode(0.5, 0.5, 1, 1, True)
    quad_tree = DensityTree(root)
    nodes = []
    for i in points:
        point_ = TreePoint(i[0], i[1])
        nodes.append(point_)
        quad_tree.insert(point_)
    return quad_tree, nodes


def build_quad_tree_by_thres(query, thres):
    print("Initial the tree with threshold " + str(thres) + "...")
    root_node = TreeNode(0.5, 0.5, 1, 1, True)
    quad_tree = DensityTree(root_node)
    quad_tree.insert_by_query(query, thres)
    return quad_tree

def build_quad_tree_by_rect(queries):
    print("Build quad tree by sampled rect queries...")
    root = TreeNode(0.5, 0.5, 1, 1, True)
    quad_tree = DensityTree(root)
    for q in queries:
        q_density = 0
        area = query_to_node(q[0] + q[1]).cal_area()
        if area > 0:
            q_density = q[2] / area
        q.append(q_density)
    queries.sort(key=lambda queries: queries[3], reverse=True)
    for q in queries:
        quad_tree.insert_by_query(q, sel_threshold)
    return quad_tree


def build_quad_tree_by_half_space(half_spaces, plane_spaces, pre_thres):
    print("Build quad tree by sampled half space queries...")
    # Pre build a tree by a rect query, this will build a uniform map
    rect_query = [[0, 0], [1, 1], 1]
    quad_tree = build_quad_tree_by_thres(rect_query, pre_thres)

    for hs in half_spaces:
        if hs[1] < 0.00001:
            quad_tree.pre_assign_by_hf(hs[0], hs[1], plane_spaces)

    print("Find " + str(undividable_n) + '/' + str(quad_tree.cal_nodes()) + " undividable buckets")

    for half_space_i in half_spaces:
        # for i in half_space_i:
        #     print(i)
        quad_tree.insert_by_half_space(half_space_i[0], half_space_i[1], plane_spaces)
    return quad_tree


def build_quad_tree_by_ball(ball_queries, pre_thres):
    print("Build quad tree by ball queries...")
    root = TreeNode(0.5, 0.5, 1, 1, True)
    plane = quad_tree_node_to_points(root)

    # Pre build a tree by a rect query, this will build a uniform map
    rect_query = [[0, 0], [1, 1], 1]
    quad_tree = build_quad_tree_by_thres(rect_query, pre_thres)

    for ball_query in ball_queries:
        ball = ball_query[0]
        sel = ball_query[1]
        inter_plane = ballPolygonIntersection(plane, ball)
        q_density = 0
        if inter_plane > 0:
            q_density = sel / inter_plane
        ball_query.append(q_density)

        # Do pre Assign some undividable labels
        if sel <= 0.00001:
            # print(ball.o.x, ball.o.y, ball.r, sel)
            quad_tree.pre_assign_by_ball(ball, sel, plane)

    print("Find " + str(undividable_n) + '/' + str(quad_tree.cal_nodes()) + " undividable buckets")
    ball_queries.sort(key=lambda queries: queries[2], reverse=True)

    for ball_query in ball_queries:
        # print(ball_query[2])
        ball = ball_query[0]
        sel = ball_query[1]
        quad_tree.insert_by_ball(ball, sel, plane)
        # print(ball.o.x, ball.o.y, ball.r, sel)
    return quad_tree


def query_to_node(query):
    q_cx = (query[0] + query[2]) / 2
    q_cy = (query[3] + query[1]) / 2
    q_width = abs(query[0] - query[2])
    q_height = abs(query[1] - query[3])
    query_node = TreeNode(q_cx, q_cy, q_width, q_height, True)
    return query_node


def quad_tree_node_to_half_space(tree_node):
    """Each rect can be rewrite to 4 half spaces"""
    corner_list = quad_tree_node_to_points(tree_node)
    # change rect to 4 half spaces, input 4 corner points
    rect_spaces = getHalfSpaces(corner_list)
    return rect_spaces


def quad_tree_node_to_points(tree_node):
    """Each rect can be rewrite to 4 points in geo"""
    cur_cx, cur_cy = tree_node.cx, tree_node.cy
    cur_w, cur_h = tree_node.w, tree_node.h
    nw_corner = [Point(cur_cx - cur_w / 2, cur_cy + cur_h / 2)]
    ne_corner = [Point(cur_cx + cur_w / 2, cur_cy + cur_h / 2)]
    se_corner = [Point(cur_cx + cur_w / 2, cur_cy - cur_h / 2)]
    sw_corner = [Point(cur_cx - cur_w / 2, cur_cy - cur_h / 2)]
    return nw_corner + ne_corner + se_corner + sw_corner


def draw(qtree, points, path):
    DPI = 72
    fig = plt.figure(figsize=(700/DPI, 500/DPI), dpi=DPI)
    ax = plt.subplot()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    # qtree.draw(ax=ax)

    ax.scatter([p.x for p in points], [p.y for p in points], s=4)
    ax.set_xticks([])
    ax.set_yticks([])

    # region = Node(140, 190, 150, 150, True)
    # found_points = []
    # qtree.query(region, found_points)
    # print('Number of found points =', len(found_points))

    # ax.scatter([p.x for p in found_points], [p.y for p in found_points],
    #            facecolors='none', edgecolors='r', s=32)
    #
    # region.draw(ax, c='r')

    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig('../results/pic' + path + str(len(qtree.get_leaf_nodes())) + '.pdf', DPI=72)
    # plt.show()


def draw_points(file_name):
    DPI = 72
    fig = plt.figure(figsize=(700 / DPI, 500 / DPI), dpi=DPI)
    ax = plt.subplot()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    count = 0

    with open(file_name, 'r') as f:
        points = []
        lines = f.readlines()

        max_sel = 0.0

        for line in lines:
            line = line.strip().split(',')
            line = [float(i) for i in line]
            sel = line[-1]
            if sel > max_sel:
                max_sel = sel
        print(max_sel)
        for line in tqdm(lines):
            line = line.strip().split(',')
            line = [float(i) for i in line]
            points.append(line)
            count += 1
            size = 4
            alpha = line[-1] * 10 + 0.3

            if alpha > 0.8:
                size = alpha * 80
                alpha = 1.0
                size += 100
            if 0.8 > alpha > 0.6:
                size = alpha * 80
                alpha += 0.2
                size += 80
            if 0.4 < alpha < 0.6:
                size = alpha * 60
                alpha += 0.2
                size += 40
            if alpha < 0.4:
                size = alpha * 200
            if line[-1] <= 0:
                alpha = 0.08
                size = 4
            if line[-1] > 0.02:
                alpha = 0.9
            if line[-1] > 0.05:
                alpha = 1.0

            ax.scatter(line[0], line[1], s=10, c='k', alpha=alpha)

        ax.set_xticks([])
        ax.set_yticks([])

        ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig('../results/pic/f4/right/f4-right-data-0.2-' + str(count) + '.pdf', DPI=72)
        # plt.show()
        return

def draw_rect(file_name):
    DPI = 72
    fig = plt.figure(figsize=(700/DPI, 500/DPI), dpi=DPI)
    ax = plt.subplot()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    count = 0

    with open(file_name, 'r') as f:
        node_list = []
        # for i in range(3):
        #     f.readline()
        lines = f.readlines()
        random.shuffle(lines)
        max_sel = 0.0

        for line in lines:
            line = line.strip().split(',')
            line = [float(i) for i in line]
            sel = line[-1]
            if sel > max_sel:
                max_sel = sel

        print(max_sel)
        for line in tqdm(lines):
            line = line.strip().split(',')
            line = [float(i) for i in line]
            node = query_to_node(line)
            # alpha = round(line[-1] / max_sel, 5)
            alpha = line[-1] * 10 + 0.3

            if alpha > 0.8:
                alpha = 1.0
            if 0.8 > alpha > 0.6:
                alpha += 0.2
            if 0.4 < alpha < 0.6:
                alpha += 0.2
            if line[-1] <= 0:
                alpha = 0.001
            if line[-1] > 0.02:
                alpha = 0.9
            if line[-1] > 0.05:
                alpha = 1.0
            if line[-1] != 0 and line[-1] / node.w / node.h < 5:
                alpha = 0.12
            node.draw(ax, alpha=alpha)

            count += 1
            if count > 500000:
                break

        ax.set_xticks([])
        ax.set_yticks([])
        ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig('../results/pic/f4/f4-middle-data-0.01-' + str(count) + '.pdf', DPI=72)
        # plt.show()
        return


"""Test draft"""
#
# nw, ne, sw, se = [Point(0.0, 1.0)], [Point(1.0, 1.0)], [Point(0.0, 0.0)], [Point(1.0, 0.0)]
# plane_spaces = getHalfSpaces(nw + ne + se + sw)


# _root = TreeNode(cx=0.5, cy=0.5, w=1, h=1, is_leaf=True)
# root_half_space = quad_tree_node_to_half_space(root)
# halfSpaces = [[Line(Point(0.5, 0.0), Point(0.0, 0.5)), 0.25], [Line(Point(0.0, 0.5), Point(0.5, 1.0)), 0.25],
#               [Line(Point(0.5, 1.0), Point(1.0, 0.5)), 0.25], [Line(Point(1.0, 0.5), Point(0.5, 0.0)), 0.25]]
# q_tree = build_quad_tree_by_half_space(half_spaces=halfSpaces, plane_spaces=root_half_space)
# draw(q_tree, [])
# draw_rect('../power_6w5.txt')

# rect_query = [[0, 0], [1, 1], 1]
# plane = quad_tree_node_to_points(_root)
# q_tree = build_quad_tree_by_rect_and_thres(rect_query, 0.1)
# o = Point(0.5, 0.5)
# r = 0.5
# ball = Ball(o, r)
# q_tree.pre_assign_by_ball(ball, 0, plane)
# for i in q_tree.get_leaf_nodes():
#     print(i.sel)

# draw_rect('../data/workload/power-2d-10001.txt')
# draw_rect('./hdcs_spl0.010000_b500000_tr1000.txt')
# draw_points('./hdps_spl0.200000_a0.100000_tr1000.txt')


with open('../data/workload/power-data-10000.txt', 'r') as f:
    points = []
    lines = f.readlines()
    random.shuffle(lines)
    for line in tqdm(lines[:1000]):
        line = line.strip().split(',')
        line = [float(i) for i in line]
        points.append(line)
    qt, qn = build_quad_tree_by_points(points)
    draw(qt, qn, path='/f4/f4-left-final-1000points')