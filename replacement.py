from fitness import evaluate_fitness
import random


def elitism_replacement(population, offspring, fitness_values, num_elites):
    """A certain number of the best individuals from the current generation are carried over to the next generation."""
    combined_population = population + offspring
    combined_fitness = fitness_values + [evaluate_fitness(ind) for ind in offspring]
    elite_indices = sorted(range(len(combined_fitness)), key=lambda i: combined_fitness[i], reverse=True)[:num_elites]
    next_generation_population = [combined_population[i] for i in elite_indices]
    return next_generation_population


def generational_replacement(offspring):
    """The entire population is replaced by the offspring generated from the current population."""
    return offspring


def steady_state_replacement(population, offspring, fitness_values, evaluate_fitness_params, next_population_size=None):
    """The least fit individuals are replaced by new offspring."""
    if not next_population_size:
        next_population_size = population

    combined_population = population + offspring
    combined_fitness_values = fitness_values + evaluate_fitness(population, *evaluate_fitness_params)
    combined_population_sorted = [x for f, x in sorted(zip(combined_fitness_values, combined_population), reverse=True)]
    next_generation_population = combined_population_sorted[:len(next_population_size)]
    return next_generation_population


def tournament_replacement(population, offspring, tournament_size, evaluate_fitness_params):
    """A subset of individuals from the combined parent and offspring populations compete in a tournament,
     and the winners form the next generation"""
    combined_population = population + offspring
    next_generation_population = []
    while len(next_generation_population) < len(population):
        tournament = random.sample(combined_population, tournament_size)
        best_individual = max(tournament, key=lambda x: evaluate_fitness(x, *evaluate_fitness_params))
        next_generation_population.append(best_individual)
    return next_generation_population


def rank_based_replacement(population, offspring):
    """Individuals are ranked based on their fitness, and replacement is done probabilistically based on these ranks."""
    combined_population = population + offspring
    combined_fitness = [evaluate_fitness(ind) for ind in combined_population]
    ranks = sorted(range(len(combined_fitness)), key=lambda i: combined_fitness[i])
    probabilities = [1 / (rank + 1) for rank in range(len(ranks))]
    total_prob = sum(probabilities)
    probabilities = [prob / total_prob for prob in probabilities]
    next_generation_population = random.choices(combined_population, probabilities, k=len(population))
    return next_generation_population


def mu_plus_lambda_replacement(population, offspring, mu):
    """The new generation is created by selecting the best μ individuals from
    the combined set of parents (μ) and offspring (λ)"""
    combined_population = population + offspring
    combined_fitness = [evaluate_fitness(ind) for ind in combined_population]
    sorted_indices = sorted(range(len(combined_fitness)), key=lambda i: combined_fitness[i], reverse=True)
    next_generation_population = [combined_population[i] for i in sorted_indices[:mu]]
    return next_generation_population


def replacement(population, offspring, fitness_values, evaluate_fitness_params, next_population_size=None):
    return steady_state_replacement(population, offspring, fitness_values, evaluate_fitness_params, next_population_size)