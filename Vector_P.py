import numpy as np
import pandas as pd


def calculate_local_p_vector(element, ambient_temperature, alfa):

    val = 0.57735

    def calculate(k, e):
        shape_functions = [0.25 * (1 - k) * (1 - e),
                           0.25 * (1 + k) * (1 - e),
                           0.25 * (1 + k) * (1 + e),
                           0.25 * (1 - k) * (1 + e)]

        return shape_functions

    def calculate_next(df):
        df = df.T
        ar = np.array(df)
        ar = ar * alfa * ambient_temperature
        return ar

    def calculate_sum(pc_list):
        a = pc_list[0] + pc_list[1]
        a = a * float(element.step_x / 2)
        return a

    # for pc in pcs:
    #     pc = [pd.DataFrame(calculate(- val, - 1)), pd.DataFrame(calculate(val, -1))]

    pc_one_list = [pd.DataFrame(calculate(- val, - 1)), pd.DataFrame(calculate(val, -1))]

    pc_one_list[0] = calculate_next(pc_one_list[0])
    pc_one_list[1] = calculate_next(pc_one_list[1])

    calculate_sum(pc_one_list)
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

    vector_p = np.zeros(4)

    if element.nodes[0].border_flag == True and element.nodes[1].border_flag == True:
        vector_p = vector_p + pow_list[0]

    if element.nodes[1].border_flag == True and element.nodes[2].border_flag == True:
        vector_p = vector_p + pow_list[1]

    if element.nodes[2].border_flag == True and element.nodes[3].border_flag == True:
        vector_p = vector_p + pow_list[2]

    if element.nodes[3].border_flag == True and element.nodes[0].border_flag == True:
        vector_p = vector_p + pow_list[3]

    return vector_p
