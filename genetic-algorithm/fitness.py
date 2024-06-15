import numpy as np
from utils import *


def fitness_boundary_constraint(layout, area_size):
    """ Evaluate the layout based on the boundary constraints."""
    boundary_penalty = 0
    for pos in layout:
        x, y = pos
        if not (0 <= x < area_size) or not (0 <= y < area_size):
            boundary_penalty += 1
    return -boundary_penalty


def fitness_uniform_spacing(layout, min_spacing):
    """Evaluate the layout based on the uniform spacing of turbines."""
    spacing_penalty = 0
    for i, pos1 in enumerate(layout):
        for pos2 in layout[i+1:]:
            distance = euclidean_distance(pos1, pos2)
            if distance < min_spacing:
                spacing_penalty += (min_spacing - distance) ** 2
    return -spacing_penalty


def power_output(wind_speed):
    """Calculate the energy production for a single turbine based on wind speed."""
    P_r = 3.00  # Rated turbine power output [MW]
    v_ci = 3.0  # Cut-in wind speed [m/s]
    v_r = 9.8  # Rated wind speed [m/s]
    v_co = 22.5  # Cut-out wind speed [m/s]

    if wind_speed < v_ci or wind_speed >= v_co:
        return 0
    elif wind_speed < v_r:
        return P_r * ((wind_speed - v_ci) / (v_r - v_ci)) ** 3
    else:
        return P_r


def is_within_wake_zone(upstream_pos, downstream_pos, wind_direction, spread_angle):
    """Check if the downstream turbine is within the wake zone of the upstream turbine."""
    wind_direction_rad = math.radians(wind_direction)
    spread_angle_rad = math.radians(spread_angle)

    dx = downstream_pos[0] - upstream_pos[0]
    dy = downstream_pos[1] - upstream_pos[1]

    turbine_angle = math.atan2(dy, dx)
    relative_angle = abs(turbine_angle - wind_direction_rad)

    if relative_angle > math.pi:
        relative_angle = 2 * math.pi - relative_angle

    if relative_angle <= spread_angle_rad:
        return True
    return False


def fitness_wake_zone_penalty(layout, wind_direction, spread_angle=10):
    """Calculate the wake effect penalty for a layout."""
    wake_penalty = 0
    for i, pos1 in enumerate(layout):
        for pos2 in layout[i+1:]:
            if is_within_wake_zone(pos1, pos2, wind_direction, spread_angle):
                wake_penalty += 1
    return -wake_penalty


def calculate_layout_energy_production(layout, wind_speed):
    rotor_radius = 136/2
    C_t = 0.89  # thrust coefficient, 0.89 for simplicity, tbd
    k_w = 0.075  # wake decay coefficient, 0.075 is typical for onshore wind farms

    total_energy = 0
    for pos1 in layout:
        wake_deficit = 0
        for pos2 in layout:
            if pos1[0] != pos2[0] or pos1[1] != pos2[1]:
                distance = euclidean_distance(pos1, pos2)
                wake_deficit += (1 - math.sqrt(1 - C_t)) * (rotor_radius / (k_w * distance + rotor_radius))**2

        effective_wind_speed = wind_speed * (1 - min(1, wake_deficit))
        total_energy += power_output(effective_wind_speed)
    return total_energy


def fitness_multi_objective(layout, weights, area_size, min_spacing, wind_speed, wind_direction):
    """Fitness with wake loss applied to energy production function."""
    energy_production = calculate_layout_energy_production(layout, wind_speed)

    boundary_fitness = fitness_boundary_constraint(layout, area_size)
    spacing_fitness = fitness_uniform_spacing(layout, min_spacing)
    is_valid = -energy_production if not is_layout_valid(layout, area_size, min_spacing) else 0

    total_fitness = (weights['energy_production'] * energy_production +
                     weights['boundary_fitness'] * spacing_fitness +
                     weights['spacing_fitness'] * boundary_fitness +
                     weights['is_valid'] * is_valid
                     )
    return total_fitness


def evaluate_fitness(population, weights, area_size, min_spacing, wind_speed, wind_direction):
    """Calculate the fitness (total energy production) for each candidate solution in the population."""

    num_bits = len(population[0][0]) // 2
    population_decoded = [[decode_binary_to_position(pos, num_bits) for pos in layout] for layout in population]

    fitness_values = []
    for layout in population_decoded:
        total_fitness = fitness_multi_objective(layout, weights, area_size, min_spacing, wind_speed, wind_direction)
        fitness_values.append(total_fitness)

    return fitness_values


def fitness_max_energy_production(layout, weights, wind_speed):
    total_energy = sum((power_output(wind_speed) for turbine in layout))
    return weights['energy_production'] * total_energy
