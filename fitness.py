from constraints import *


# def power_output(turbine_coordinates, wind_speed):
#     """
#     Calculate the energy production for a single turbine based on its position and wind speed.
#     #AEP
#
#     Parameters:
#         turbine_coordinates (tuple): Tuple containing the (x, y) coordinates of the turbine.
#         wind_speed (float): Wind speed at the turbine location.
#
#     Returns:
#         float: Energy production for the turbine.
#     """
#     # alpha = 0.5
#     # beta = 0.03
#     P_r = 3.35  # Rated turbine power output [MW]
#     v_ci = 4.0  # Cut-in wind speed [m/s]
#     v_r = 9.8  # Rated wind speed [m/s]
#     v_co = 25.0  # Cut-out wind speed [m/s]
#
#     # TMP
#     if turbine_coordinates[1]:
#         wind_speed *= turbine_coordinates[0] / turbine_coordinates[1]
#
#     if wind_speed < v_ci or wind_speed >= v_co:
#         return 0
#     elif wind_speed < v_r:
#         return P_r * ((wind_speed - v_ci) / (v_r - v_ci)) ** 3
#     else:
#         return P_r
def power_output(turbine_coordinates, wind_speed):
    return -abs(turbine_coordinates[0] - turbine_coordinates[1])


def calculate_layout_energy_production(layout, wind_speed):
    """Calculate the energy production for turbine layout."""
    total_energy = sum((power_output(coordinates, wind_speed) for coordinates in layout))
    return total_energy


def evaluate_fitness(population, area_size, min_spacing, wind_speed):
    """Calculate the fitness (total energy production) for each candidate solution in the population."""

    num_bits = len(population[0][0]) // 2
    population_decoded = [[decode_binary_to_position(pos, num_bits) for pos in layout] for layout in population]

    fitness_values = []
    for layout in population_decoded:
        if is_layout_valid(layout, area_size, min_spacing):
            total_energy = calculate_layout_energy_production(layout, wind_speed)
        else:
            total_energy = float('-inf')   # penalty
        fitness_values.append(total_energy)

    return fitness_values
