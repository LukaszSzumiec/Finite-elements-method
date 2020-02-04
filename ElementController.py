from jacobian_2d import *
from Matrix_H import *
from Matrix_C import calculate_matrix_c
from Matrix_HBC_2D import calculate_matrix_hbc
from Vector_P import calculate_local_p_vector


def calculate_local_h_matrix(element):
    x = [element.nodes[0].x,
         element.nodes[1].x,
         element.nodes[2].x,
         element.nodes[3].x]
    y = [element.nodes[0].y,
         element.nodes[1].y,
         element.nodes[2].y,
         element.nodes[3].y]

    dn_dksi, dn_deta = calculate_shape_function(2)
    jacobian = calculate_jacobian(x, y, dn_dksi, dn_deta)
    element.det_j = calculate_det_of_j(jacobian)
    JJ = calculate_matrix(jacobian, element.det_j)
    dn_dx, dn_dy = calculate_dn_dx_dn_dy(dn_dksi, dn_deta, JJ)

    dn_dx_h, dn_dy_h = first_step(dn_dx, dn_dy)
    dn_dx_h, dn_dy_h = multiply_by_det(dn_dx_h, dn_dy_h, element.det_j)

    h_matrix = calculate_h_matrix(third_step(dn_dx_h, dn_dy_h))

    return h_matrix


def calculate_local_matrix_c(element):

    shape_functions = calculate_shape_functions_values()

    return calculate_matrix_c(shape_functions, element.det_j)


def calculate_local_hbc2d_and_add_to_h(element, CONVECTION):

    return calculate_matrix_hbc(element, CONVECTION, element.det_j)


def calculate_local_p(element, ambient_temperature, alfa):

    return calculate_local_p_vector(element, ambient_temperature, alfa)
