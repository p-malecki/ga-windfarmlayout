import random
import math
import numpy as np
from fitness import evaluate_fitness
from selection import selection
from crossover import crossover
from mutation import mutation
from replacement import replacement
from constraints import *
from utils import *
from plotting import *


def initialize_population(population_size, n_turbines, area_size, min_spacing, max_attempts=100):
    """Generate random turbine layouts with each turbine within the land area and satisfying spacing constraints."""

    initial_population = []
    max_coordinate = area_size  # - min_spacing
    num_bits = determine_num_bits(area_size)

    for _ in range(population_size):
        layout = []
        for _ in range(n_turbines):
            x = random.randint(0, max_coordinate)
            y = random.randint(0, max_coordinate)

            attempts = 0
            while attempts < max_attempts:
                x = random.randint(0, max_coordinate)
                y = random.randint(0, max_coordinate)

                is_new_position_valid = True
                for pos in layout:
                    if not is_valid_spacing(pos, (x, y), min_spacing):
                        is_new_position_valid = False
                        break
                if is_new_position_valid:
                    layout.append((x, y))
                    break
                attempts += 1
            else:
                raise RuntimeError("Maximum attempts reached without finding a valid position.")

        encoded_layout = [encode_position_to_binary(pos[0], pos[1], num_bits) for pos in layout]
        initial_population.append(encoded_layout)

    return initial_population


def genetic_algorithm(ga_config):
    """Run the genetic algorithm"""

    n_turbines = ga_config['n_turbines']
    area_size = ga_config['area_size']
    min_spacing = ga_config['min_spacing']
    max_attempts = ga_config['max_attempts']
    wind_speed = ga_config['wind_speed']
    population_size = ga_config['population_size']
    mutation_rate = ga_config['mutation_rate']
    max_generations = ga_config['max_generations']
    max_stagnation = ga_config['max_stagnation']

    solutions_fitness_values = []
    solutions_layouts = []
    best_result = [float('-inf'), -1]
    best_result_generation = 0
    stagnation_counter = 0

    num_bits = determine_num_bits(area_size)
    population = initialize_population(population_size, n_turbines, area_size, min_spacing, max_attempts)

    # main GA loop
    for generation in range(max_generations):

        fitness_values = evaluate_fitness(population, area_size, min_spacing, wind_speed)

        # Update best result
        current_best_result = max(zip(fitness_values, range(len(fitness_values))))
        current_layout = [decode_binary_to_position(pos, num_bits) for pos in population[current_best_result[1]]]
        solutions_fitness_values.append(current_best_result[0])
        solutions_layouts.append(current_layout)
        if current_best_result[0] > best_result[0]:
            best_result = current_best_result
            best_result_generation = generation
            print(f'>>> Generation {generation} best result {best_result[0]}')
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

        # print("fitness_values", max(fitness_values), fitness_values.count(float('-inf')), end=" ")
        # print_population(population, "population")
        # print_population(selected_parents, "selected_parents:")
        # print_population(offspring, "offspring")
        # print_population(mutated_offspring, "mutated_offspring")

        evaluate_fitness_params = (area_size, min_spacing, wind_speed)
        population = replacement(population, mutated_offspring, fitness_values, evaluate_fitness_params)
        # print_population(population, "replacement")

    best_fitness = best_result[0]
    best_layout = [decode_binary_to_position(pos, num_bits) for pos in population[best_result[1]]]
    print(f"Best result found: P = {best_fitness} MW")
    print(f"Best turbines layout found: {best_layout}")
    print(f'Generation of best result {best_result_generation}')
    print('-' * 40)
    # plot_turbine_layout(best_layout_pos)

    return (best_fitness, best_layout), (solutions_fitness_values, solutions_layouts)

