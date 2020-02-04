import pandas as pd
import numpy as np

c = 700
ro = 7800


def calculate_matrix_c(shape_function, det):
    shape_function = shape_function.T

    matrix = []

    for x in range(4):
        single_row_x = pd.DataFrame(shape_function[x])
        single_row_x_T = pd.DataFrame(shape_function[x]).T
        field = single_row_x.dot(single_row_x_T)
        field = np.array(field)
        field = field * np.float32(det[x]) * ro * c
        matrix.append(field)

    matrix_c = np.zeros((4, 4))

    for x in range(4):
        for y in range(4):
            matrix_c[x][y] = round(matrix[0][x][y] + matrix[1][x][y] + matrix[2][x][y] + matrix[3][x][y], 5)

    return pd.DataFrame(matrix_c)
