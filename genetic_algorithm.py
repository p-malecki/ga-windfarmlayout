import random
import math
import numpy as np
from utils import *
from plotting import *
import random


def initialize_population(population_size, n_turbines, area_size, min_spacing, max_attempts=100):
    """
    Generate random turbine layouts with each turbine within the land area and satisfying spacing constraints.

    Parameters:
        population_size (int): Number of individuals in the population.
        n_turbines (int): Number of turbines (N).
        area_size (int): Size of the land area (assuming a square area) (L).
        min_spacing (float): Minimum spacing between turbines (D).
        max_attempts (int): Maximum number of attempts to find a valid position for a new turbine.

    Returns:
        list: A list of turbine layouts, where each layout is represented as a list of (x, y) coordinates.
    """
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

                is_new_possition_valid = True
                for pos in layout:
                    if not is_valid_spacing(pos, (x, y), min_spacing):
                        is_new_possition_valid = False
                        break
                if is_new_possition_valid:
                    layout.append((x, y))
                    break
                attempts += 1
            else:
                raise RuntimeError("Maximum attempts reached without finding a valid position.")

        encoded_layout = [encode_position_to_binary(pos[0], pos[1], num_bits) for pos in layout]
        initial_population.append(encoded_layout)

    return initial_population


def power_output(turbine_coordinates, wind_speed):
    """
    Calculate the energy production for a single turbine based on its position and wind speed.
    #AEP

    Parameters:
        turbine_coordinates (tuple): Tuple containing the (x, y) coordinates of the turbine.
        wind_speed (float): Wind speed at the turbine location.

    Returns:
        float: Energy production for the turbine.
    """
    # alpha = 0.5
    # beta = 0.03
    P_r = 3.35  # Rated turbine power output [MW]
    v_ci = 4.0  # Cut-in wind speed [m/s]
    v_r = 9.8  # Rated wind speed [m/s]
    v_co = 25.0  # Cut-out wind speed [m/s]

    # TMP
    if turbine_coordinates[1]:
        wind_speed *= turbine_coordinates[0] / turbine_coordinates[1]

    if wind_speed < v_ci or wind_speed >= v_co:
        return 0
    elif wind_speed < v_r:
        return P_r * ((wind_speed - v_ci) / (v_r - v_ci)) ** 3
    else:
        return P_r


def calculate_layout_energy_production(layout, wind_speed):
    """Calculate the energy production for turbine layout."""
    total_energy = sum((power_output(coordinates, wind_speed) for coordinates in layout))
    return total_energy


def evaluate_fitness(population, area_size, min_spacing, wind_speed):
    """
    Calculate the fitness (total energy production) for each candidate solution in the population.

    Parameters:
        population (list): List of turbine layouts, where each layout is represented as a list of (x, y) coordinates.
        area_size (int): Size of the land area (assuming a square area) (L).
        min_spacing (float): Minimum spacing between turbines (D).
        wind_speed (float): Wind speed at the turbine location. (V)

    Returns:
        list: List of fitness values for each candidate solution in the population.
    """
    fitness_values = []
    for layout in population:
        total_energy = 0
        if is_layout_valid(layout, area_size, min_spacing):
            total_energy = calculate_layout_energy_production(layout, wind_speed)
        fitness_values.append(total_energy)

    return fitness_values


def tournament_selection(population, tournament_size):
    pass


def selection(population, fitness_values):
    """Perform selection of individuals from the population based on their fitness values."""
    total_fitness = sum(fitness_values)
    probabilities = [fitness / total_fitness for fitness in fitness_values] if total_fitness else []

    selected_population = []
    for _ in range(len(population)):
        selected_individual = roulette_wheel_select(population, probabilities)
        selected_population.append(selected_individual)

    return selected_population


def roulette_wheel_select(population, probabilities):
    """Perform roulette wheel selection to select an individual from the population based on probabilities."""
    spin = random.random()
    cumulative_probability = 0
    for individual, probability in zip(population, probabilities):
        cumulative_probability += probability
        if spin <= cumulative_probability:
            return individual


def onepoint_crossover(parents):
    """Perform crossover to create offspring from parent individuals using single-point crossover."""
    offspring = []
    for i in range(0, len(parents) - 1, 2):
        parent1 = parents[i]
        parent2 = parents[i+1]

        crossover_point = random.randint(1, len(parent1) - 1)
        offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
        offspring2 = parent2[:crossover_point] + parent1[crossover_point:]

        offspring.append(offspring1)
        offspring.append(offspring2)
    return offspring


def twopoint_crossover(parents):
    """Perform crossover to create offspring from parent individuals using two-point crossover."""
    offspring = []
    for i in range(0, len(parents) - 1, 2):
        parent1 = parents[i]
        parent2 = parents[i+1]

        cut_spot_1 = random.randint(1, len(parent1) - 1)
        cut_spot_2 = random.randint(1, len(parent1) - 1)
        offspring1 = parent1[:cut_spot_1] + parent2[cut_spot_1:cut_spot_2] + parent1[cut_spot_2:]
        offspring2 = parent2[:cut_spot_1] + parent1[cut_spot_1:cut_spot_2] + parent2[cut_spot_2:]

        offspring.append(offspring1)
        offspring.append(offspring2)
    return offspring


def mutation(offspring, mutation_rate):
    """Perform mutation on offspring individuals with a given mutation rate."""
    mutated_offspring = []
    for individual in offspring:
        mutated_individual = ''
        for gene in individual:
            if random.random() < mutation_rate:
                mutated_gene = '0' if gene == '1' else '1'
            else:
                mutated_gene = gene
            mutated_individual += mutated_gene
        mutated_offspring.append(mutated_individual)
    return mutated_offspring


def replacement(population, offspring, fitness_values, next_population_size=None):
    """Perform replacement to select individuals for the next generation based on fitness values."""
    if not next_population_size:
        next_population_size = population

    combined_population = population + offspring
    combined_population_sorted = [x for _, x in sorted(zip(fitness_values, combined_population), reverse=True)]
    next_generation_population = combined_population_sorted[:len(next_population_size)]
    return next_generation_population


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

    best_result = [float('-inf'), -1]
    stagnation_counter = 0

    num_bits = determine_num_bits(area_size)
    population = initialize_population(population_size, n_turbines, area_size, min_spacing, max_attempts)

    # main GA loop
    for generation in range(max_generations):

        population_decoded = [[decode_binary_to_position(pos, num_bits) for pos in layout] for layout in population]
        fitness_values = evaluate_fitness(population_decoded, area_size, min_spacing, wind_speed)

        # Check for stagnation
        current_best_result = max(zip(fitness_values, range(len(fitness_values))))
        print('current_best_result', current_best_result)
        if current_best_result[0] > best_result[0]:
            best_result = current_best_result
            print(f'    Generation {generation} best result {best_result[0]}')
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        if stagnation_counter >= max_stagnation:
            print(f"Terminating due to stagnation at generation {generation+1}.\n")
            break
        if generation == max_generations - 1:
            print(f"Terminating due to reaching maximum of {generation+1} generations.\n")
            break

        # Next population
        selected_parents = selection(population, fitness_values)
        offspring = onepoint_crossover(selected_parents)
        mutated_offspring = mutation(offspring, mutation_rate)
        population = replacement(population, mutated_offspring, fitness_values)

    best_layout = population[best_result[1]]
    best_layout_pos = [decode_binary_to_position(pos, num_bits) for pos in best_layout]
    print(f"Best result found: P = {best_result[0]} MW")
    print(f"Best turbines layout found: {best_layout_pos}")
    plot_turbine_layout(best_layout_pos)
