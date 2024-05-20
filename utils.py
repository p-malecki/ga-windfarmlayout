import math


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


def euclidean_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


def print_population(population, title=''):
    print(title)
    num_bits = len(population[0][0]) // 2
    for i, layout in enumerate(population):
        print(i, [decode_binary_to_position(pos, num_bits) for pos in layout])
