from pathlib import Path

CASES = [("../inputs/day1_example.txt",), ("../inputs/day1.txt",)]

STARTING_POSITION = 50
DIAL_POSITIONS = 100


def solve(input_path: str | Path):
    input_path = Path(input_path)
    print(f"Solving {input_path.stem}")

    # Open input file and read all lines
    with open(input_path, "r", encoding="utf-8") as file:
        rotations = file.readlines()

    # Map to pairs of direction, distance
    rotations = [[line[0], int(line[1:])] for line in rotations]

    # PART 1
    current_pos = STARTING_POSITION  # Dial position
    zero_hits = 0  # i.e. the password

    # For each rotation...
    for dir, dist in rotations:
        # Apply it and wrap if needed
        if dir == "L":
            current_pos -= dist
        else:
            current_pos += dist
        current_pos %= DIAL_POSITIONS

        # Increment if landed on 0
        if current_pos == 0:
            zero_hits += 1

    # Print result
    print(f"Part 1: {zero_hits}")

    # PART 2
    current_pos = STARTING_POSITION  # Dial position
    zero_hits = 0  # i.e. the password

    # For each rotation...
    for dir, dist in rotations:
        # Increment hits for each full rotation, and remove them
        zero_hits += dist // DIAL_POSITIONS
        dist %= DIAL_POSITIONS

        # Apply remaining rotation
        if dir == "L":
            # If this would reach 0 or beyond, and dial isn't already on 0,
            # increment hits
            if dist >= current_pos and current_pos != 0:
                zero_hits += 1
            current_pos -= dist
        else:
            # If this would reach 0 or beyond,
            # increment hits
            if current_pos + dist >= DIAL_POSITIONS:
                zero_hits += 1
            current_pos += dist

        # Wrap if needed
        current_pos %= 100

    # Print result
    print(f"Part 2: {zero_hits}")


# Run for each input
for case in CASES:
    solve(*case)
    print("=" * 64)
