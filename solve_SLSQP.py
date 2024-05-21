import numpy as np
from scipy.optimize import minimize
from utils import generate_random_correct_layout
from fitness import power_output, fitness_multi_objective
from plotting import *

# PROBLEM DEFINITION
n_turbines = 14
area_size = 300
min_spacing = 50
wind_speed = 9.8
wind_direction = 270.0


# fitness_weights = {
#         'energy_production': 0.5,
#         'boundary_fitness': 0.2,
#         'spacing_fitness': 0.2,
#         'wake_fitness': 0.1,
#     }
fitness_weights = {
        'energy_production': 1,
        'boundary_fitness': 1,
        'spacing_fitness': 1,
        'wake_fitness': 1,
    }
deficit_coefficient = 0.05  # Wake decay constant
turbine_diameter = 80  # Assumed diameter of wind turbines in meters


def calculate_layout_energy_production(layout, wind_speed):
    total_energy = 0
    for i in range(n_turbines):
        wake_deficit = 0
        for j in range(n_turbines):
            if i != j:
                distance = np.sqrt((layout[i, 0] - layout[j, 0])**2 + (layout[i, 1] - layout[j, 1])**2)
                if distance < (2 * turbine_diameter):
                    wake_deficit += (1 - np.sqrt(1 - deficit_coefficient * ((turbine_diameter / distance)**2)))

        effective_wind_speed = wind_speed * (1 - wake_deficit)
        energy_production = sum((power_output(turbine, effective_wind_speed) for turbine in layout))
        total_energy += energy_production
    return total_energy


def objective_function(flattened_layout, wind_speed):
    layout = flattened_layout.reshape((n_turbines, 2)).astype(int)
    fitness_value = fitness_multi_objective(layout, fitness_weights, area_size, min_spacing, wind_speed, wind_direction)
    print("Objective function value: ", fitness_value)
    return -fitness_value


# def constraint_boundary(layout):
#     layout = layout.reshape((n_turbines, 2))
#     x, y = layout[:, 0], layout[:, 1]
#     return np.concatenate([x, area_size - x, y, area_size - y])
#
#
# def constraint_spacing(layout):
#     layout = layout.reshape((n_turbines, 2))
#     min_distances = []
#     for i, (x1, y1) in enumerate(layout):
#         for j, (x2, y2) in enumerate(layout):
#             if i != j:
#                 min_distances.append(np.sqrt((x2 - x1)**2 + (y2 - y1)**2) - min_spacing)
#     return np.array(min_distances)
#
#
# boundary_constraints = {
#     'type': 'ineq',
#     'fun': constraint_boundary
# }
#
# spacing_constraints = {
#     'type': 'ineq',
#     'fun': constraint_spacing
# }

np.random.seed(42)
initial_layout = generate_random_correct_layout(n_turbines, area_size, min_spacing)
#initial_layout = [[0, 0]] * n_turbines
print(initial_layout)

# Optimize using SLSQP
initial_flattened_layout = np.array(initial_layout).flatten()
result = minimize(objective_function,
                  initial_flattened_layout,
                  args=(wind_speed),
                  method='SLSQP',
                  #constraints=[boundary_constraints, spacing_constraints],
                  options={'maxiter': 100, 'disp': True})

optimal_layout = result.x.reshape((n_turbines, 2))
optimal_layout = np.rint(optimal_layout).astype(int)

print("Optimal Layout:\n", optimal_layout)
plot_turbine_layout(optimal_layout)
plot_multiple_layouts([optimal_layout, initial_layout])
print(result)

