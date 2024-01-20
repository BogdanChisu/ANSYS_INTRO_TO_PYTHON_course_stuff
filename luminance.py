import sys
import numpy as np

def find_data_cross_section(simulation_filename):
    simulation = np.loadtxt(fname=simulation_filename, skiprows=52)

    x_simulation = simulation[:, 0]
    y_simulation = simulation[:, 1]
    L_simulation = simulation[:, 2]

    smallest_y = np.amin(abs(y_simulation))
    x_cross_section = x_simulation[y_simulation == smallest_y]
    luminance_cross_section = L_simulation[y_simulation == smallest_y]

    return x_cross_section, luminance_cross_section

def calculate_average_luminance(x, luminance):
    boolean_array = np.logical_and(x <= 10., x >= -10.)
    average_luminance = np.mean(luminance[boolean_array])

    return average_luminance

def calculate_std_luminance(x, luminance):
    boolean_array = np.logical_and(x <= 10., x >= -10.)
    std_luminance = np.std(luminance[boolean_array])
    return std_luminance

def load_experiment_data(experiment_filename):
    experiment = np.loadtxt(fname=experiment_filename, delimiter=',')
    return experiment[:, 0], experiment[:, 1]



def calculate_luminance_stats(x, luminance, action):
    boolean_array = np.logical_and(x <= 10, x >= -10)
    if action == '--mean':
        statistic = np.mean(luminance[boolean_array])
    elif action == '--std':
        statistic = np.std(luminance[boolean_array])
    else:
        raise TypeError('No valid action supplied (allowed actions are "--mean" or "--std")')
    return statistic

def main():
    action1 = sys.argv[1]
    action2 = sys.argv[2]

    if action2 == '--experiment':
        experiment_filename = sys.argv[3]
        x_experiment, luminance_experiment = load_experiment_data(experiment_filename)
        filenames = sys.argv[4:]
    else:
        experiment_filename = ''
        filenames = sys.argv[2:]

    print(filenames)
    for filename in filenames:
        x, luminance = find_data_cross_section(filename)
        simulation_statistic = calculate_luminance_stats(x, luminance, action1)
        print(action1[2:] + ' luminance for ' + filename + ' = ' + str(simulation_statistic) + ' Cd/m^2')
        if bool(experiment_filename):
            experiment_statistic = calculate_luminance_stats(x_experiment, luminance_experiment, action1)
            perc_diff = (experiment_statistic - simulation_statistic) * 100 / experiment_statistic
            print('Percentage difference with experimental value = ' + str(perc_diff) + ' %')

# print(sys.argv)

# print(__name__)

if __name__ == '__main__':
    main()