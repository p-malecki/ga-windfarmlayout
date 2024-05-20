import random


def onepoint_layouts_pair_crossover(parents):
    """Perform single-point crossover to create offspring from consecutive pair of parents."""
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


def onepoint_layouts_crossover(parents):
    """Perform single-point crossover to create offspring for each parent with random one. Split layouts."""
    offspring = []
    for i in range(len(parents)):
        random_index = random.choice([j for j in range(len(parents)) if j != i])
        parent1 = parents[i]
        parent2 = parents[random_index]

        crossover_point = random.randint(1, len(parent1) - 1)
        offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
        offspring2 = parent2[:crossover_point] + parent1[crossover_point:]

        offspring.append(offspring1)
        offspring.append(offspring2)
    return offspring


def twopoint_layouts_crossover(parents):
    """Perform crossover to create offspring from parent individuals using two-point crossover. Split layouts."""
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


def onepoint_position_crossover(parents):
    """Create offspring for each parent with random one. Split combined x,y position strings in random point."""
    offspring = []
    for i in range(len(parents)):
        random_index = random.choice([j for j in range(len(parents)) if j != i])
        parent1 = parents[i]
        parent2 = parents[random_index]

        offspring1, offspring2 = [], []
        for turbine_index in range(len(parent1)):
            crossover_point = random.randint(1, len(parent1) - 1)
            offspring1.append(parent1[turbine_index][:crossover_point] + parent2[turbine_index][crossover_point:])
            offspring2.append(parent2[turbine_index][:crossover_point] + parent1[turbine_index][crossover_point:])
        offspring.append(offspring1)
        offspring.append(offspring2)
    return offspring


def onepoint_coordinate_crossover(parents):
    """Create offspring for each parent with random one. Split each x and y position string in random point."""
    offspring = []
    for i in range(len(parents)):
        random_index = random.choice([j for j in range(len(parents)) if j != i])
        parent1 = parents[i]
        parent2 = parents[random_index]

        offspring1, offspring2 = [], []
        for turbine in range(len(parent1)):
            cord_separator = len(parent1)//2
            crossover_point_x = random.randint(1, cord_separator - 1)
            crossover_point_y = random.randint(cord_separator, len(parent1) - 1)
            offspring1_x = parent1[turbine][:crossover_point_x] + parent2[turbine][crossover_point_x:cord_separator]
            offspring1_y = parent1[turbine][cord_separator:crossover_point_y] + parent2[turbine][crossover_point_y:]
            offspring2_x = parent2[turbine][:crossover_point_x] + parent1[turbine][crossover_point_x:cord_separator]
            offspring2_y = parent2[turbine][cord_separator:crossover_point_y] + parent1[turbine][crossover_point_y:]
            offspring1.append(offspring1_x + offspring1_y)
            offspring2.append(offspring2_x + offspring2_y)
        offspring.append(offspring1)
        offspring.append(offspring2)
    return offspring


def crossover(parents):
    return onepoint_position_crossover(parents)
    #return onepoint_coordinate_crossover(parents)
