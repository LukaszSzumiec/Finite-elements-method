from ElementController import *
import math


class Grid(object):

    def __init__(self, h, b, n_h, n_b, temperature):
        super(Grid, self).__init__()
        self.global_h = h
        self.global_b = b
        self.global_n_h = n_h
        self.global_n_b = n_b
        self.elements = []
        self.nodes = []

        self.global_h_matrix = np.zeros((n_h * n_b, n_b * n_b))
        self.global_c_matrix = np.zeros((n_h * n_b, n_b * n_b))
        self.global_p_vector = np.zeros((n_h * n_b))

        self.initialize_nodes(n_h, n_b)
        self.initialize_elements(n_h, n_b)

    def initialize_nodes(self, n_h, n_b):

        step_x = round(self.global_h / (self.global_n_h - 1), 10)
        step_y = round(self.global_b / (self.global_n_b - 1), 10)

        for i in range(n_h * n_b):
            x = 0
            y = 0
            local_id = i
            while True:
                if step_y * local_id <= self.global_b:
                    y += step_y * local_id
                    break
                local_id -= self.global_n_b
                x += step_x
            x = round(x, 10)
            y = round(y, 10)
            self.nodes.append(Node(x, y, i))

    def initialize_elements(self, n_h, n_b):

        number_of_elements = (n_h - 1) * (n_b - 1)

        local_elements = []
        for elements_number in range(number_of_elements):
            local_elements.append(Element(elements_number + 1, self.global_h, self.global_b, n_h, n_b, self))

        self.elements = local_elements

    def get_node_by_coords(self, searched_x, searched_y):
        for node in self.nodes:
            if math.isclose(node.x, searched_x, abs_tol=0.001) and math.isclose(node.y, searched_y, abs_tol=0.001):
                return node


class Element(object):

    def __init__(self, element_id, h, b, n_h, n_b, grid):
        super(Element, self).__init__()
        self.id = element_id
        self.global_h = h
        self.global_b = b
        self.global_n_h = n_h
        self.global_n_b = n_b
        self.grid = grid
        self.x = -1
        self.y = -1
        self.det_j = None
        self.step_x = -1
        self.step_y = -1
        self.nodes = []
        self.calculate_x_and_y_coords_of_element()
        self.initialize_nodes()
        self.calculate_border_flag()

        self.local_h_matrix = calculate_local_h_matrix(self)
        self.local_c_matrix = calculate_local_matrix_c(self)

    def calculate_x_and_y_coords_of_element(self):

        step_x = self.step_x = round(self.global_h / (self.global_n_h - 1), 10)
        step_y = self.step_y = round(self.global_b / (self.global_n_b - 1), 10)

        local_id = self.id
        self.x = round(step_x / 2, 10)
        self.y = round(step_y / 2, 10)
        while True:
            if step_y * local_id < self.global_b:
                self.y = step_y * local_id - round(step_y / 2, 10)
                break
            local_id -= self.global_n_b - 1
            self.x += step_x
        self.x = round(self.x, 10)
        self.y = round(self.y, 10)

    def initialize_nodes(self):
        self.nodes = [self.grid.get_node_by_coords(self.x - (self.step_x / 2), self.y - (self.step_y / 2)),
                      self.grid.get_node_by_coords(self.x + (self.step_x / 2), self.y - (self.step_y / 2)),
                      self.grid.get_node_by_coords(self.x + (self.step_x / 2), self.y + (self.step_y / 2)),
                      self.grid.get_node_by_coords(self.x - (self.step_x / 2), self.y + (self.step_y / 2))]

    def calculate_border_flag(self):
        for node in self.nodes:
            node.add_element(self)

    def __str__(self):
        return f'{"Element no.:", self.id, "x:", self.x, "y:", self.y}'


class Node(object):

    def __init__(self, x, y, node_id):
        super(Node, self).__init__()
        self.x = x
        self.y = y
        self.border_flag = None
        self.id = node_id

    def add_element(self, element):
        self.border_flag = self.is_border(element.global_h, element.global_b)

    def __str__(self):
        return f'{self.x, " ", self.y}'

    def __repr__(self):
        return f'{self.x, " ", self.y}'

    def is_border(self, h, b):

        if math.isclose(self.x, 0, abs_tol=0.001) or math.isclose(self.x, h, abs_tol=0.001):
            return True
        elif math.isclose(self.y, 0, abs_tol=0.001) or math.isclose(self.y, h, abs_tol=0.001):
            return True
        return False
