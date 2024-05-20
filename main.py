from genetic_algorithm import *
from plotting import *


# set figsize and dpi for all figures
# plt.rcParams["figure.figsize"] = (5, 5)
# plt.rcParams["figure.dpi"] = 90


ga_config = {
    'n_turbines': 10,
    'area_size': 1300,
    'min_spacing': 100,
    'max_attempts': 100,
    'wind_speed': 9.8,
    'population_size': 1000,
    'mutation_rate': 0.1,
    'max_generations': 100,
    'max_stagnation': 50,
}

ga_config_fast = {
    'n_turbines': 5,
    'area_size': 1000,
    'min_spacing': 100,
    'max_attempts': 100,
    'wind_speed': 9.8,
    'population_size': 100,
    'mutation_rate': 0.1,
    'max_generations': 50,
    'max_stagnation': 50,
}


if __name__ == '__main__':
    solutions_best_fitness_values = []
    solutions_best_layouts = []
    solutions_fitness_values = []
    solutions_layouts = []
    for i in range(2):
        print(f"ITERATION {i+1}")
        (best_fitness, best_layout), (fitness_values, layouts) = genetic_algorithm(ga_config)
        # (best_fitness, best_layout), (fitness_values, layouts) = genetic_algorithm(ga_config_fast)
        solutions_best_fitness_values.append([i+1, best_fitness])
        solutions_best_layouts.append(best_layout)
        solutions_fitness_values.append(fitness_values)
        solutions_layouts.append(layouts)
    print('\nsolutions_best_fitness_values: ', solutions_best_fitness_values)

    plot_population_layouts(solutions_best_layouts, title=f'Best turbine layouts')

    for i, fitness_values in enumerate(solutions_fitness_values):
        plt.plot(fitness_values, label=f'solution {i+1}')
    plt.title(f'Fitness scores across generations {solutions_best_fitness_values}')
    plt.legend(loc='lower right')
    plt.show()

    for i, layouts in enumerate(solutions_layouts):
        plot_population_layouts(layouts[::10], title=f'Turbine layouts {i+1}', alpha_ascending=True)

