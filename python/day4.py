from itertools import product
from pathlib import Path

CASES = [("../inputs/day4_example.txt",), ("../inputs/day4.txt",)]


def solve(input_path: str | Path):
    input_path = Path(input_path)
    print(f"Solving {input_path.stem}")

    # Open input file and read all lines
    with open(input_path, "r", encoding="utf-8") as file:
        grid = file.read().splitlines()

    # Convert str to list[str] so they're mutable
    grid = [list(row) for row in grid]

    rows = len(grid)
    cols = len(grid[0])

    # PART 1
    rolls = 0

    # Just check as described.

    # For each coord in the grid
    for i, j in product(range(rows), range(cols)):
        # If it's a roll,
        if grid[i][j] == "@":
            # Count number of adjacent rolls:
            num_adjacent = 0
            # For each of the directions,
            for di, dj in product([-1, 0, 1], [-1, 0, 1]):
                # If it's not just the same coord, and is in grid bounds,
                if (di, dj) != (0, 0) and 0 <= i + di < rows and 0 <= j + dj < cols:
                    # Increment num adjacent if a roll is at the coord
                    if grid[i + di][j + dj] == "@":
                        num_adjacent += 1

            # If fewer than 4, increment
            if num_adjacent < 4:
                rolls += 1

    # Print result
    print(f"Part 1: {rolls}")

    # PART 2
    rolls = 0

    # Do same as above, but keep track of removable rolls,
    # remove them at the end, and repeat until none left

    while True:
        # Removable rolls on this iteration
        removable = []
        # For each coord in the grid
        for i, j in product(range(rows), range(cols)):
            # If it's a roll,
            if grid[i][j] == "@":
                # Count number of adjacent rolls:
                num_adjacent = 0
                # For each of the directions,
                for di, dj in product([-1, 0, 1], [-1, 0, 1]):
                    # If it's not just the same coord, and is in grid bounds,
                    if (di, dj) != (0, 0) and 0 <= i + di < rows and 0 <= j + dj < cols:
                        # Increment num adjacent if a roll is at the coord
                        if grid[i + di][j + dj] == "@":
                            num_adjacent += 1

                # If fewer than 4, increment and record it
                if num_adjacent < 4:
                    rolls += 1
                    removable.append((i, j))

        # If none removable, done
        if len(removable) == 0:
            break

        # Remove all the removable rolls
        for i, j in removable:
            grid[i][j] = "."

    # Print result
    print(f"Part 2: {rolls}")


# Run for each input
for case in CASES:
    solve(*case)
    print("=" * 64)
