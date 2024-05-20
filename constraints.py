from utils import *


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
