import math
import random


def determine_num_bits(max_coordinate):
    """Calculate the number of bits required to represent the maximum coordinate value."""
    num_bits = math.ceil(math.log2(max_coordinate))
    return num_bits


def encode_position_to_binary(x, y, num_bits):
    """Encode the (x, y) coordinates to a binary string."""
    x_binary = format(x, '0' + str(num_bits) + 'b')
    y_binary = format(y, '0' + str(num_bits) + 'b')
    binary_string = x_binary + y_binary
    return binary_string


def decode_binary_to_position(binary_string, num_bits):
    """Decode the binary string to (x, y) coordinates."""
    x_binary = binary_string[:num_bits]
    y_binary = binary_string[num_bits:]
    x = int(x_binary, 2)
    y = int(y_binary, 2)
    return x, y


def decode_layout_to_position(layout):
    num_bits = len(layout[0]) // 2
    return [decode_binary_to_position(pos, num_bits) for pos in layout]


def euclidean_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


def print_population(population, title=''):
    print(title)
    num_bits = len(population[0][0]) // 2
    for i, layout in enumerate(population):
        print(i, [decode_binary_to_position(pos, num_bits) for pos in layout])


def generate_random_correct_layout(n_turbines, area_size, min_spacing, max_attempts=100):
    max_coordinate = area_size  # - min_spacing
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
                layout.append([x, y])
                break
            attempts += 1
        else:
            raise RuntimeError("Maximum attempts reached without finding a valid position.")
    return layout


def generate_random_incorrect_layout(n_turbines, area_size, min_spacing, max_attempts=100):
    max_coordinate = area_size  # - min_spacing
    layout = []
    for _ in range(n_turbines):
        x = random.randint(0, max_coordinate)
        y = random.randint(0, max_coordinate)
        layout.append([x, y])
    return layout


def is_valid_spacing(pos1, pos2, min_spacing):
    """Check if turbines at the positions satisfy the minimum spacing constraint."""
    return euclidean_distance(pos1, pos2) >= min_spacing


def is_position_within_bounds(position, area_size):
    """Check if a position is within the bounds of the specified area."""
    x, y = position
    return 0 <= x <= area_size and 0 <= y <= area_size


def is_layout_valid(layout, area_size, min_spacing):
    """Check if the entire layout satisfies the minimum spacing constraint and is within the bounds of the area."""

    for i, pos1 in enumerate(layout):
        if not is_position_within_bounds(pos1, area_size):
            return False
        for pos2 in layout[i+1:]:
            if not is_valid_spacing(pos1, pos2, min_spacing):
                return False
    return True


def initialize_population(population_size, n_turbines, area_size, min_spacing, max_attempts=100):
    """Generate random turbine layouts with each turbine within the land area and satisfying spacing constraints."""

    initial_population = []
    num_bits = determine_num_bits(area_size)
    for _ in range(population_size):
        layout = generate_random_incorrect_layout(n_turbines, area_size, min_spacing, max_attempts)
        encoded_layout = [encode_position_to_binary(pos[0], pos[1], num_bits) for pos in layout]
        initial_population.append(encoded_layout)

    return initial_population
