from Model import Grid
from ElementController import *


def calculate_global_h_matrix(grid: Grid, conductivity, alfa):

    for element in grid.elements:
        element.local_h_matrix = calculate_local_h_matrix(element=element)
        element.local_h_matrix += calculate_local_hbc2d_and_add_to_h(element=element, CONVECTION=alfa)

        nodes_id = []
        for node in element.nodes:
            nodes_id.append(node.id)

        for i in range(4):
            for k in range(4):
                val = element.local_h_matrix[i, k]
                grid.global_h_matrix[nodes_id[i], nodes_id[k]] += val


def calculate_global_c_matrix(grid: Grid, conductivity, alfa):

    for element in grid.elements:
        element.local_c_matrix = np.array(calculate_local_matrix_c(element=element))

        nodes_id = []
        for node in element.nodes:
            nodes_id.append(node.id)

        for i in range(4):
            for k in range(4):
                val = element.local_c_matrix[i, k]
                grid.global_c_matrix[nodes_id[i], nodes_id[k]] += val


def calculate_global_p_vector(grid: Grid, ambient_temperature, alfa):

    for element in grid.elements:
        nodes_id = []
        for node in element.nodes:
            nodes_id.append(node.id)

        element.local_p_vector = calculate_local_p(element, ambient_temperature, alfa)

        i = 0
        for val in np.nditer(element.local_p_vector):
            grid.global_p_vector[nodes_id[i]] += val
            i += 1
