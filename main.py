from genetic_algorithm import *
from plotting import *


# set figsize and dpi for all figures
# plt.rcParams["figure.figsize"] = (5, 5)
# plt.rcParams["figure.dpi"] = 90


# PROBLEM DEFINITION
n_turbines = 14
area_size = 300
min_spacing = 50
wind_speed = 9.8
wind_direction = 270.0


ga_config = {
    'n_turbines': n_turbines,
    'area_size': area_size,
    'min_spacing': min_spacing,
    'wind_speed': wind_speed,
    'wind_direction': wind_direction,
    'population_size': 100,
    'mutation_rate': 0.01,
    'max_generations': 250,
    'max_stagnation': 20,
    'fitness_weights': {
        'energy_production': 1,
        'boundary_fitness': 1,
        'spacing_fitness': 1,
        'wake_fitness': 10,
    }
}


if __name__ == '__main__':
    solutions_best_fitness_values = []
    solutions_best_layouts = []
    solutions_max_fitness_values = []
    solutions_avg_fitness_values = []
    solutions_layouts = []
    global_best_solution = 0
    for i in range(1):
        print(f"ITERATION {i+1}")
        gbs, (best_fitness, best_layout), (fitness_max_values, layouts), fitness_avg_values = genetic_algorithm(ga_config)
        solutions_best_fitness_values.append([i+1, best_fitness])
        solutions_best_layouts.append(best_layout)
        solutions_max_fitness_values.append(fitness_max_values)
        solutions_avg_fitness_values.append(fitness_avg_values)
        solutions_layouts.append(layouts)
        global_best_solution = gbs
    print('\nsolutions_best_fitness_values: ', solutions_best_fitness_values, global_best_solution)

    # plot_multiple_layouts(solutions_best_layouts, title=f'Best turbine layouts')
    # for i, layouts in enumerate(solutions_layouts):
    #     plot_multiple_layouts(layouts[::10], title=f'Turbine layouts {i + 1}', alpha_ascending=True)

    plot_solutions_data_stats(solutions_max_fitness_values,
                              title='Fitness max scores across generations {solutions_best_fitness_values}',
                              axhline=global_best_solution)
    plot_solutions_data_stats(solutions_avg_fitness_values,
                              title='Fitness average scores', axhline=global_best_solution)

    print('Are solutions_best_layouts valid?')
    for i, layout in enumerate(solutions_best_layouts):
        print(f"solution {i+1} valid:", is_layout_valid(layout, area_size, min_spacing))
