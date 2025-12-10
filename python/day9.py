from itertools import combinations
from pathlib import Path

CASES = [("../inputs/day9_example.txt",), ("../inputs/day9.txt",)]


def solve(input_path: str | Path):
    input_path = Path(input_path)
    print(f"Solving {input_path.stem}")

    # Open input file and read all lines
    with open(input_path, "r", encoding="utf-8") as file:
        input_str = file.readlines()

    # Split into pairs of x, y coords
    red_tiles = [[int(coord) for coord in row.split(",")] for row in input_str]

    num_tiles = len(red_tiles)
    print(f"Input contains {num_tiles} tiles")

    # PART 1
    largest = 0

    for (x1, y1), (x2, y2) in combinations(red_tiles, 2):
        area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        largest = max(largest, area)

    # Print result
    print(f"Part 1: {largest}")

    # PART 2
    part2_v1(red_tiles)


def cross(v1: tuple[int, int], v2: tuple[int, int]) -> int:
    return v1[0] * v2[1] - v1[1] * v2[0]


# First solution (gets the right answer, but bad...very convoluted and inefficient, might be wrong)
def part2_v1(red_tiles: list[list[int]]):
    num_tiles = len(red_tiles)

    # For this solution, +x is right, +y is up, unlike the example visual.

    # Determine which side of the edges the green tiles are on.
    # For example, without knowing this, (2, 5), (9, 7) in the example could be a rectangle.
    #
    # To do this, take any edge along the bounding box of the polygon
    # (must exist on each side), here the x_min side is used...

    # Min x of the polygon
    bb_x_min = min(x for x, _ in red_tiles)

    # Find an edge along this x...
    is_cw = None
    for i in range(num_tiles - 1):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[i + 1]

        # Found one
        if x1 == x2 == bb_x_min:
            # If this edge is going up, the tiles are in clockwise order,
            # otherwise counterclockwise.
            #
            # Traveling in this same direction along the loop,
            # the green tiles stay on the same side.
            # (CW = on right, CCW = on left)
            is_cw = y2 > y1
            break

    assert is_cw is not None

    largest = 0
    best_pair = None

    # Returns True iff, when traveling along the tiles in order
    # from index start to end, the end tile is never on the inner side
    # of the edge (the green side).
    #
    # When this is True, the rect formed by these two tiles is entirely
    # outside the polygon.
    def end_never_on_inner_side(start, end) -> bool:
        x_end, y_end = red_tiles[end]

        # Iterate through all edges [from, to] in order,
        # starting from start, possibly wrapping around the tile list
        t_from = start
        while t_from != end:
            t_to = (t_from + 1) % num_tiles
            x_from, y_from = red_tiles[t_from]
            x_to, y_to = red_tiles[t_to]

            # Get cross product of this edge and [from, end]
            # to determine direction of end relative to this edge
            cross_prod = cross(
                (x_to - x_from, y_to - y_from), (x_end - x_from, y_end - y_from)
            )
            # If end is on the inner side...
            # If traveling CW, the cross product would be negative
            # If CCW, positive.
            # In this case, return False.
            if cross_prod != 0 and (cross_prod < 0) == is_cw:
                return False

            t_from = t_to  # Equivalent to increment
        return True

    # Returns True iff any edge of the polygon crosses inside the rect
    # formed by the given tiles (only overlapping on the side doesn't count).
    def any_edge_crosses_rect(p_min: tuple[int, int], p_max: tuple[int, int]) -> bool:
        for i in range(num_tiles):
            edge_x1, edge_y1 = red_tiles[i]
            edge_x2, edge_y2 = red_tiles[(i + 1) % num_tiles]
            edge_x_min, edge_x_max = sorted([edge_x1, edge_x2])
            edge_y_min, edge_y_max = sorted([edge_y1, edge_y2])

            if (
                edge_x_min < p_max[0]
                and edge_x_max > p_min[0]
                and edge_y_min < p_max[1]
                and edge_y_max > p_min[1]
            ):
                return True

        return False

    # For each tile, take it as the first corner of a rectangle...
    for t1 in range(num_tiles):
        x1, y1 = red_tiles[t1]
        # Then each tiles coming after as the second,
        # but only if it's the short way around (halfway or less through the list)
        for steps in range(1, num_tiles // 2 + 1):
            t2 = (t1 + steps) % num_tiles
            x2, y2 = red_tiles[t2]

            # Order their coords
            x_min, x_max = sorted([x1, x2])
            y_min, y_max = sorted([y1, y2])

            # If any edge crosses through the rectangle, it's not valid
            if any_edge_crosses_rect((x_min, y_min), (x_max, y_max)):
                continue

            # Still need to deal with concave cases like (2, 5), (9, 7) in example
            # If, traveling along the polygon between them (the short way),
            # the second corner is never on the inner side,
            # the whole rect is outside, i.e. the concave case
            # (THIS IS THE MOST DUBIOUS PART)
            if end_never_on_inner_side(t1, t2):
                continue

            # This is a valid rect, so compute the area and check for max
            area = (x_max - x_min + 1) * (y_max - y_min + 1)
            if area > largest:
                largest = area
                best_pair = (x1, y1), (x2, y2)

    # Print result
    print(f"Part 2: {largest}, formed by {best_pair}")


# Run for each input
for case in CASES:
    solve(*case)
    print("=" * 64)
