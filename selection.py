import random


def base_selection(population, fitness_values):
    """Perform selection of individuals from the population based on their fitness values."""
    total_fitness = sum([(f if f > float('-inf') else 0) for f in fitness_values])
    if not total_fitness:
        probabilities = [1 / len(population)] * len(population)
    else:
        probabilities = [(f / total_fitness if f > float('-inf') else 0) for f in fitness_values]

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


def tournament_selection(population, tournament_size):
    pass


def selection(population, fitness_values):
    return base_selection(population, fitness_values)