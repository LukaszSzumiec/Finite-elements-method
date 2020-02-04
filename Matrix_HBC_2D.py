import pandas as pd
import numpy as np


def calculate_matrix_hbc(element, CONVECTION, det_j):
    val = 0.57735

    def calculate(k, e):
        shape_functions = [0.25 * (1 - k) * (1 - e),
                           0.25 * (1 + k) * (1 - e),
                           0.25 * (1 + k) * (1 + e),
                           0.25 * (1 - k) * (1 + e)]

        return shape_functions

    def calculate_next(df):
        df_t = df.T
        df = df.dot(df_t)
        array = np.array(df)
        array = array * CONVECTION
        return array

    def calculate_sum(pc_list):
        a = pc_list[0] + pc_list[1]
        det = element.step_x / 2
        a = a * det
        return a

    pc_one_list = [pd.DataFrame(calculate(- val, - 1)), pd.DataFrame(calculate(val, -1))]

    pc_one_list[0] = calculate_next(pc_one_list[0])
    pc_one_list[1] = calculate_next(pc_one_list[1])

    pow_list = [calculate_sum(pc_one_list)]

    # PC 2

    pc_two_list = [pd.DataFrame(calculate(1, - val)), pd.DataFrame(calculate(1, val))]

    pc_two_list[0] = calculate_next(pc_two_list[0])
    pc_two_list[1] = calculate_next(pc_two_list[1])

    pow_list.append(calculate_sum(pc_two_list))

    # PC 3

    pc_three_list = [pd.DataFrame(calculate(val, 1)), pd.DataFrame(calculate(- val, 1))]

    pc_three_list[0] = calculate_next(pc_three_list[0])
    pc_three_list[1] = calculate_next(pc_three_list[1])

    pow_list.append(calculate_sum(pc_three_list))

    # PC 4

    pc_four_list = [pd.DataFrame(calculate(- 1, val)), pd.DataFrame(calculate(- 1, - val))]

    pc_four_list[0] = calculate_next(pc_four_list[0])
    pc_four_list[1] = calculate_next(pc_four_list[1])

    pow_list.append(calculate_sum(pc_four_list))

    matrix_hbc = np.zeros((4, 4))

    if element.nodes[0].border_flag == True and element.nodes[1].border_flag == True:
        matrix_hbc = matrix_hbc + pow_list[0]

    if element.nodes[1].border_flag == True and element.nodes[2].border_flag == True:
        matrix_hbc = matrix_hbc + pow_list[1]

    if element.nodes[2].border_flag == True and element.nodes[3].border_flag == True:
        matrix_hbc = matrix_hbc + pow_list[2]

    if element.nodes[3].border_flag == True and element.nodes[0].border_flag == True:
        matrix_hbc = matrix_hbc + pow_list[3]

    return matrix_hbc
