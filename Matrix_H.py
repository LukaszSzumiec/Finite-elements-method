import pandas as pd
import numpy as np

CONDUCTIVITY = 25


# {dN / dx} * {dN / dx}T
# {dN / dy} * {dN / dy}T
def first_step(dn_dx, dn_dy):
    dn_dx = pd.DataFrame(dn_dx).T
    dn_dy = pd.DataFrame(dn_dy).T

    dn_dx_H = []
    dn_dy_H = []

    def calculate(df, df_t):
        return df.dot(df_t)

    for x in range(4):
        single_row_x = pd.DataFrame(dn_dx[x])
        single_row_x_T = pd.DataFrame(dn_dx[x]).T
        dn_dx_H.append(calculate(single_row_x, single_row_x_T))

        single_row_y = pd.DataFrame(dn_dy[x])
        single_row_y_T = pd.DataFrame(dn_dy[x]).T
        dn_dy_H.append(calculate(single_row_y, single_row_y_T))

    return dn_dx_H, dn_dy_H


# ( {dN / dx} * {dN / dx}T ) * det_j
# ( {dN / dy} * {dN / dy}T ) * det_j
def multiply_by_det(dn_dx_h, dn_dy_h, det):
    for x in range(4):
        array_x = np.array(dn_dx_h[x].values)
        array_x = array_x * np.float32(det[x])
        dn_dx_h[x] = pd.DataFrame(array_x)

        array_y = np.array(dn_dy_h[x].values)
        array_y = array_y * np.float32(det[x])
        dn_dy_h[x] = pd.DataFrame(array_y)

    return dn_dx_h, dn_dy_h


# ( {dN / dx} * {dN / dx}T ) * det_j * CONDUCTIVITY
# ( {dN / dy} * {dN / dy}T ) * det_j * CONDUCTIVITY
def calculate_k_matrix(dn_dx_h, dn_dy_h):
    def calculate(matrix_x, matrix_y):
        matrix = [[], [], [], []]
        for z in range(4):
            for y in range(4):
                matrix[z].append(round(CONDUCTIVITY * (matrix_x[z][y] + matrix_y[z][y]), 10))
        return matrix

    k_matrix = []
    for x in range(4):
        k_matrix.append(pd.DataFrame(calculate(dn_dx_h[x], dn_dy_h[x])))

    return k_matrix


# Sum k matrix
def calculate_h_matrix(k_matrix):
    h_matrix = np.zeros((4, 4))

    for x in range(4):
        for y in range(4):
            h_matrix[x][y] = round(k_matrix[0][x][y] + k_matrix[1][x][y] + k_matrix[2][x][y] + k_matrix[3][x][y], 5)

    return h_matrix
