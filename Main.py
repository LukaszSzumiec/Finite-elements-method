from GridController import *


def calc(h, b, n_h, n_b, simulation_time, step_time,
         ambient_temperature, alfa, specific_heat, density, conductivity, initial_temperature):
    grid = Grid(h, b, n_h, n_b, initial_temperature)

    t_0 = np.zeros(n_b * n_h)
    for i in range(n_b * n_b):
        t_0[i] = initial_temperature

    for i in range(0, int(simulation_time / step_time), 1):
        calculate_global_h_matrix(grid, conductivity, alfa)
        calculate_global_c_matrix(grid, conductivity, alfa)
        calculate_global_p_vector(grid, ambient_temperature, alfa)
        step_matrix = np.divide(grid.global_c_matrix, step_time)
        h_matrix = grid.global_h_matrix + step_matrix
        p_matrix = grid.global_p_vector + (step_matrix.dot(t_0))
        t_1 = np.linalg.solve(h_matrix, p_matrix)
        print(f'{"Time:", i * step_time + step_time, "Min temp:", round(np.amin(t_1), 3), "Max temp:", round(np.amax(t_1), 3)}')

        t_0 = np.copy(t_1)
        grid.global_c_matrix = np.zeros((n_b * n_b, n_b * n_b))
        grid.global_h_matrix = np.zeros((n_b * n_b, n_b * n_b))
        grid.global_p_vector = np.zeros(n_b * n_b)


def load_data_from_file(filepath: str):
    arg_tab = []
    with open(filepath) as f:
        for line in f:
            arg_tab.append(float(line))

    print(arg_tab)
    if len(arg_tab) != 12:
        return

    calc(h=arg_tab[0], b=arg_tab[1], n_h=int(arg_tab[2]), n_b=int(arg_tab[3]), simulation_time=int(arg_tab[4]),
         step_time=int(arg_tab[5]), ambient_temperature=arg_tab[6], alfa=arg_tab[7], specific_heat=arg_tab[8],
         density=arg_tab[9], conductivity=arg_tab[10], initial_temperature=arg_tab[11])


def main():

    # Case 1

    # calc(h=0.1, b=0.1, n_h=4, n_b=4, simulation_time=500, step_time=50, ambient_temperature=1200,
    #      alfa=300, specific_heat=700, density=7800, conductivity=25, initial_temperature=100)

    # Case 1

    load_data_from_file("data")

    # Case 2
    print("Starting case 2...")
    calc(h=0.1, b=0.1, n_h=31, n_b=31, simulation_time=100, step_time=1, ambient_temperature=1200,
         alfa=300, specific_heat=700, density=7800, conductivity=25, initial_temperature=100)


if __name__ == '__main__':
    main()
