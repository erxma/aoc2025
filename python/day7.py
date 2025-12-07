from collections import Counter
from pathlib import Path

CASES = [("../inputs/day7_example.txt",), ("../inputs/day7.txt",)]


def solve(input_path: str | Path):
    input_path = Path(input_path)
    print(f"Solving {input_path.stem}")

    # Open input file and read all lines
    with open(input_path, "r", encoding="utf-8") as file:
        grid = file.read().splitlines()

    # Convert each row's str to list[str] so they're mutable
    grid = [list(row) for row in grid]

    # Get starting column
    start_col = grid[0].index("S")

    # PART 1
    num_splits = 0

    # Simulate travel of beams as described, all traveling row by row together
    beamed_cols = {start_col}  # Set of all columns with a beam in it on current row
    # For each row after the first...
    for row in grid[:-1]:
        # Get list of columns where a split occurs,
        # i.e. a splitter exists and is hit (has a beam above it)
        split_cols = list(filter(lambda col: row[col] == "^", beamed_cols))

        # Add to tally of splits
        num_splits += len(split_cols)

        # For each of the splits...
        for split_col in split_cols:
            # Remove the beam traveling on the column
            beamed_cols.remove(split_col)
            # Add the new beams on the left and right
            # (can assume they won't go out of bounds)
            beamed_cols.add(split_col - 1)
            beamed_cols.add(split_col + 1)

    # Print result
    print(f"Part 1: {num_splits}")

    # PART 2

    # Similar to Part 1, but instead track the number of timelines
    # that each col currently has a beam at
    beamed_cols = Counter({start_col: 1})

    # For each row after the first...
    for row in grid[:-1]:
        # Get list of columns where a split occurs,
        # i.e. a splitter exists and is hit (has a beam above it)
        split_cols = list(filter(lambda col: row[col] == "^", beamed_cols.keys()))

        # For each of the columns with splits...
        for split_col in split_cols:
            # Get number of timelines here
            timelines_at_col = beamed_cols[split_col]
            # The beam on this col disappears in all timelines
            beamed_cols[split_col] = 0
            # Now, for each beam that split,
            # there's one timeline on the left and one on the right
            # (can assume they won't go out of bounds)
            beamed_cols[split_col - 1] += timelines_at_col
            beamed_cols[split_col + 1] += timelines_at_col

    num_timelines = beamed_cols.total()

    # Print result
    print(f"Part 2: {num_timelines}")


# Run for each input
for case in CASES:
    solve(*case)
    print("=" * 64)
