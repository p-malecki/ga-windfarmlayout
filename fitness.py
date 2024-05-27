from utils import *


def power_output(turbine_coordinates, wind_speed):
    """Calculate the energy production for a single turbine based on its position and wind speed."""
    P_r = 3.35  # Rated turbine power output [MW]
    v_ci = 4.0  # Cut-in wind speed [m/s]
    v_r = 9.8  # Rated wind speed [m/s]
    v_co = 25.0  # Cut-out wind speed [m/s]

    if wind_speed < v_ci or wind_speed >= v_co:
        return 0
    elif wind_speed < v_r:
        return P_r * ((wind_speed - v_ci) / (v_r - v_ci)) ** 3
    else:
        return P_r


def calculate_layout_energy_production(layout, wind_speed):
    total_energy = sum((power_output(turbine, wind_speed) for turbine in layout))
    return total_energy


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


def is_within_wake_zone(upstream_pos, downstream_pos, wind_direction, spread_angle):
    """Check if the downstream turbine is within the wake zone of the upstream turbine."""
    wind_direction_rad = math.radians(wind_direction)
    spread_angle_rad = math.radians(spread_angle)

    dx = downstream_pos[0] - upstream_pos[0]
    dy = downstream_pos[1] - upstream_pos[1]

    # Calculate the angle between the line connecting the turbines and the wind direction
    turbine_angle = math.atan2(dy, dx)
    relative_angle = abs(turbine_angle - wind_direction_rad)

    # Normalize the relative angle to the range [0, pi]
    if relative_angle > math.pi:
        relative_angle = 2 * math.pi - relative_angle

    # Check if the downstream turbine is within the wake spread angle
    if relative_angle <= spread_angle_rad:
        return True
    return False

# def calculate_layout_energy_production(layout, wind_speed):
#     total_energy = 0
#     for i in range(n_turbines):
#         wake_deficit = 0
#         for j in range(n_turbines):
#             if i != j:
#                 distance = np.sqrt((layout[i, 0] - layout[j, 0])**2 + (layout[i, 1] - layout[j, 1])**2)
#                 if distance < (2 * turbine_diameter):
#                     wake_deficit += (1 - np.sqrt(1 - deficit_coefficient * ((turbine_diameter / distance)**2)))
#
#         effective_wind_speed = wind_speed * (1 - wake_deficit)
#         energy_production = sum((power_output(turbine, effective_wind_speed) for turbine in layout))
#         total_energy += energy_production
#     return total_energy


def fitness_wake_effect(layout, wind_direction, spread_angle=10):
    """Calculate the wake effect penalty for a layout."""
    wake_penalty = 0
    for i, pos1 in enumerate(layout):
        for pos2 in layout[i+1:]:
            if is_within_wake_zone(pos1, pos2, wind_direction, spread_angle):
                wake_penalty += 1
    return -wake_penalty


def fitness_multi_objective(layout, weights, area_size, min_spacing, wind_speed, wind_direction):
    """Evaluate the layout based on multiple objectives."""
    energy_production = calculate_layout_energy_production(layout, wind_speed)
    boundary_fitness = fitness_boundary_constraint(layout, area_size)
    spacing_fitness = fitness_uniform_spacing(layout, min_spacing)
    wake_fitness = fitness_wake_effect(layout, wind_direction)
    is_valid = -1 if not is_layout_valid(layout, area_size, min_spacing) else 0
    # print(f'fitness_multi_objective: {round(energy_production)}\t{boundary_fitness}\t{round(spacing_fitness)}\t\t{round(wake_fitness)}')

    total_fitness = (weights['energy_production'] * energy_production +
                     weights['boundary_fitness'] * spacing_fitness +
                     weights['spacing_fitness'] * boundary_fitness +
                     weights['wake_fitness'] * wake_fitness +
                     weights['is_valid'] * is_valid
                     )
    return total_fitness


def fitness_max_energy_production(layout, weights, wind_speed):
    return weights['energy_production'] * calculate_layout_energy_production(layout, wind_speed)


def evaluate_fitness(population, weights, area_size, min_spacing, wind_speed, wind_direction):
    """Calculate the fitness (total energy production) for each candidate solution in the population."""

    num_bits = len(population[0][0]) // 2
    population_decoded = [[decode_binary_to_position(pos, num_bits) for pos in layout] for layout in population]

    # use fitness_multi_objective (v2)
    fitness_values = []
    for layout in population_decoded:
        total_fitness = fitness_multi_objective(layout, weights, area_size, min_spacing, wind_speed, wind_direction)
        fitness_values.append(total_fitness)

    # use calculate_layout_energy_production (v1)
    # for layout in population_decoded:
    #     if is_layout_valid(layout, area_size, min_spacing):
    #         total_energy = calculate_layout_energy_production(layout, wind_speed)
    #     else:
    #         total_energy = float('-inf')  # penalty
    #     fitness_values.append(total_energy)

    return fitness_values



