import numpy as np
import pandas as pd


def calculate_jacobian(x, y, ksi_array, eta_array):
    def calculate(coord, array):
        a = (array[0] * coord[0]) + (array[1] * coord[1]) + (array[2] * coord[2]) + (array[3] * coord[3])
        return a

    jacobian = [[], [], [], []]

    jacobian[0].append(calculate(x, ksi_array[0]))
    jacobian[0].append(calculate(y, ksi_array[0]))
    jacobian[0].append(calculate(x, eta_array[0]))
    jacobian[0].append(calculate(y, eta_array[0]))

    jacobian[1].append(calculate(x, ksi_array[1]))
    jacobian[1].append(calculate(y, ksi_array[1]))
    jacobian[1].append(calculate(x, eta_array[1]))
    jacobian[1].append(calculate(y, eta_array[1]))

    jacobian[2].append(calculate(x, ksi_array[1]))
    jacobian[2].append(calculate(y, ksi_array[1]))
    jacobian[2].append(calculate(x, eta_array[1]))
    jacobian[2].append(calculate(y, eta_array[1]))

    jacobian[3].append(calculate(x, ksi_array[1]))
    jacobian[3].append(calculate(y, ksi_array[1]))
    jacobian[3].append(calculate(x, eta_array[1]))
    jacobian[3].append(calculate(y, eta_array[1]))

    jacobian = pd.DataFrame(jacobian)
    jacobian = jacobian.T

    return jacobian


def calculate_det_of_j(jacobian):
    def calculate(sub_matrix):
        return sub_matrix[3] * sub_matrix[0] - sub_matrix[2] * sub_matrix[1]

    det = []
    for x in range(4):
        det.append(calculate(jacobian[x]))
    det = pd.DataFrame(det)
    det = det.T
    return det


def calculate_shape_function(number_of_integral_points):
    def calculate_dNdksi(ksi, eta):
        dNdksi = []
        dNdksi.append(-ksi * 0.25 * (1 - eta))
        dNdksi.append(ksi * 0.25 * (1 - eta))
        dNdksi.append(ksi * 0.25 * (1 + eta))
        dNdksi.append(-ksi * 0.25 * (1 + eta))
        return dNdksi

    def calculate_dNdeta(eta, ksi):
        dNdeta = [-eta * 0.25 * (1 - ksi),
                  -eta * 0.25 * (1 + ksi),
                  eta * 0.25 * (1 + ksi),
                  eta * 0.25 * (1 - ksi)]
        return dNdeta

    if number_of_integral_points == 2:
        ksi = 0.577350269
        eta = 0.577350269

        d_n_d_ksi = [calculate_dNdksi(1, - ksi),
                     calculate_dNdksi(1, - ksi),
                     calculate_dNdksi(1, ksi),
                     calculate_dNdksi(1, ksi)]

        d_n_d_eta = [calculate_dNdeta(1, - eta), calculate_dNdeta(1, eta), calculate_dNdeta(1, eta),
                     calculate_dNdeta(1, - eta)]

        return d_n_d_ksi, d_n_d_eta


def calculate_shape_functions_values(ksi=0.577350269, eta=0.577350269):
    # shape_functions_array = np.zeros((4,4))

    shape_functions_list = []

    def calculate(k, e):
        shape_functions = []
        shape_functions.append(0.25 * (1 - k) * (1 - e))
        shape_functions.append(0.25 * (1 + k) * (1 - e))
        shape_functions.append(0.25 * (1 + k) * (1 + e))
        shape_functions.append(0.25 * (1 - k) * (1 + e))

        return shape_functions

    shape_functions_list.append(calculate(- ksi, - eta))
    shape_functions_list.append(calculate(ksi, - eta))
    shape_functions_list.append(calculate(ksi, eta))
    shape_functions_list.append(calculate(- ksi, eta))
    return pd.DataFrame(shape_functions_list)


def calculate_matrix(jacobian, det):
    jacobian = jacobian.T
    for index, column in jacobian.iterrows():
        for x in range(4):
            column[x] = column[x] / det[x]

    jacobian = jacobian.T
    return jacobian


def calculate_dn_dx_dn_dy(d_n_d_ksi, d_n_d_eta, JJ):
    dn_dx = [[], [], [], []]
    dn_dy = [[], [], [], []]

    for x in range(4):
        dn_dx[0].append(JJ[0][0] * d_n_d_ksi[0][x] + JJ[0][1] * d_n_d_eta[0][x])
        dn_dx[1].append(JJ[1][0] * d_n_d_ksi[1][x] + JJ[1][1] * d_n_d_eta[1][x])
        dn_dx[2].append(JJ[2][0] * d_n_d_ksi[2][x] + JJ[2][1] * d_n_d_eta[2][x])
        dn_dx[3].append(JJ[3][0] * d_n_d_ksi[3][x] + JJ[3][1] * d_n_d_eta[3][x])

    for x in range(4):
        dn_dy[0].append(JJ[0][2] * d_n_d_ksi[0][x] + JJ[0][3] * d_n_d_eta[0][x])
        dn_dy[1].append(JJ[1][2] * d_n_d_ksi[1][x] + JJ[1][3] * d_n_d_eta[1][x])
        dn_dy[2].append(JJ[2][2] * d_n_d_ksi[2][x] + JJ[2][3] * d_n_d_eta[2][x])
        dn_dy[3].append(JJ[3][2] * d_n_d_ksi[3][x] + JJ[3][3] * d_n_d_eta[3][x])

    return dn_dx, dn_dy
