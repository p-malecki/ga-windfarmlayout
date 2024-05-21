import matplotlib.pyplot as plt

from fitness import evaluate_fitness, calculate_layout_energy_production
from selection import selection
from crossover import crossover
from mutation import mutation
from replacement import replacement
from utils import *
from plotting import *


def initialize_population(population_size, n_turbines, area_size, min_spacing, max_attempts=100):
    """Generate random turbine layouts with each turbine within the land area and satisfying spacing constraints."""

    initial_population = []
    num_bits = determine_num_bits(area_size)
    for _ in range(population_size):
        layout = generate_random_incorrect_layout(n_turbines, area_size, min_spacing, max_attempts)
        #layout = generate_random_correct_layout(n_turbines, area_size, min_spacing, max_attempts)
        encoded_layout = [encode_position_to_binary(pos[0], pos[1], num_bits) for pos in layout]
        initial_population.append(encoded_layout)

    return initial_population


def genetic_algorithm(ga_config):
    """Run the genetic algorithm"""

    n_turbines = ga_config['n_turbines']
    area_size = ga_config['area_size']
    min_spacing = ga_config['min_spacing']
    wind_speed = ga_config['wind_speed']
    wind_direction = ga_config['wind_direction']
    fitness_weights = ga_config['fitness_weights']

    population_size = ga_config['population_size']
    mutation_rate = ga_config['mutation_rate']
    max_generations = ga_config['max_generations']
    max_stagnation = ga_config['max_stagnation']
    fitness_params = (fitness_weights, area_size, min_spacing, wind_speed, wind_direction)

    solutions_max_fitness_values = []
    solutions_avg_fitness_values = []
    solutions_layouts = []
    best_result = [float('-inf'), -1]
    best_result_generation = 0
    stagnation_counter = 0

    population = initialize_population(population_size, n_turbines, area_size, min_spacing)
    global_best_solution = calculate_layout_energy_production(population[0], wind_speed)

    # main GA loop
    for generation in range(max_generations):
        print(f'>>> Generation {generation}')

        fitness_values = evaluate_fitness(population, *fitness_params)

        # Update best result
        current_best_result = max(zip(fitness_values, range(len(fitness_values))))
        current_avg_result = sum(fitness_values) / len(fitness_values)
        current_layout = decode_layout_to_position(population[current_best_result[1]])
        solutions_max_fitness_values.append(current_best_result[0])
        solutions_avg_fitness_values.append(current_avg_result)
        solutions_layouts.append(current_layout)
        if current_best_result[0] > best_result[0]:
            best_result, best_result_generation = current_best_result, generation
            print(f'>>>>>> new best result {best_result[0]}/{global_best_solution}')
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        # Check for stagnation
        if stagnation_counter >= max_stagnation:
            print(f"Terminating due to stagnation at generation {generation+1}.\n")
            break
        if generation == max_generations - 1:
            print(f"Terminating due to reaching maximum of {generation+1} generations.\n")
            break

        # Next population
        selected_parents = selection(population, fitness_values)
        offspring = crossover(selected_parents)
        mutated_offspring = mutation(offspring, mutation_rate, verbose=False)
        population = replacement(population, mutated_offspring, fitness_values, fitness_params)
        # print_population(population)

    best_fitness = best_result[0]
    best_layout = decode_layout_to_position(population[best_result[1]])
    print(f"Best result found: P = {best_fitness} MW")
    print(f"Best turbines layout found: {best_layout}")
    print(f'Generation of best result {best_result_generation}')
    print('-' * 40)
    # plot_turbine_layout(best_layout_pos, title="best_layout_pos")
    # plot_turbine_layout(decode_layout_to_position(population[0]), title="Last generation 1st layout")
    # plot_multiple_layouts([decode_layout_to_position(l) for l in population[::100]], title="Last generation layouts")


    return (global_best_solution,
            (best_fitness, best_layout),
            (solutions_max_fitness_values, solutions_layouts),
            solutions_avg_fitness_values)

