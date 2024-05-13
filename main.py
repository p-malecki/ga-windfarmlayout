from genetic_algorithm import *
from plotting import *


# set figsize and dpi for all figures
plt.rcParams["figure.figsize"] = (5,5)
plt.rcParams["figure.dpi"] = 90


# Parameters:
# population_size (int): Number of individuals in the population.
# n_turbines (int): Number of turbines (N).
# area_size (int): Size of the land area in meters (assuming a square area) (L).
# min_spacing (float): Minimum spacing between turbines (D).
#   No turbine can be less than two rotor diameters from any other turbine [m].
# max_attempts (int): Maximum number of attempts to find a valid position for a new turbine.

ga_config = {
    'n_turbines': 16,
    'area_size': 1300,
    'min_spacing': 100,
    'max_attempts': 100,
    'wind_speed': 9.8,
    'population_size': 3,
    'mutation_rate': 0.1,
    'max_generations': 50,
    'max_stagnation': 50,
}


if __name__ == '__main__':
    genetic_algorithm(ga_config)