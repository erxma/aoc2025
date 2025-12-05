from pathlib import Path

CASES = [("../inputs/day5_example.txt",), ("../inputs/day5.txt",)]


def solve(input_path: str | Path):
    input_path = Path(input_path)
    print(f"Solving {input_path.stem}")

    fresh_ranges = []
    available = []

    # Open input file and read all lines
    with open(input_path, "r", encoding="utf-8") as file:
        # For each line until the empty line, parse as fresh ID range
        while line := file.readline().rstrip():
            fresh_ranges.append([int(id) for id in line.split("-")])

        # The rest are available ingredient IDs
        while line := file.readline().rstrip():
            available.append(int(line))

    print(f"{len(fresh_ranges)} fresh ranges")
    print(f"{len(available)} available IDs")

    # PART 1
    # Just linear search for a matching range for each of the available IDs:
    num_fresh = 0

    # For each available ID, if it falls within any fresh range, increment tally
    for id in available:
        if any(lo <= id <= hi for [lo, hi] in fresh_ranges):
            num_fresh += 1

    # Print result
    print(f"Part 1: {num_fresh}")

    # PART 2
    # Deal with overlapping ranges by sorting the ranges and merging them

    # Sort by low end
    sorted_ranges = sorted(fresh_ranges, key=lambda r: r[0])

    num_fresh = 0
    # The max high end of a range so far.
    # It can be shown that all fresh IDs at or below this have definitely been counted
    max_hi = -1
    # For each fresh range...
    for lo, hi in sorted_ranges:
        # If the high end is greater than the max already seen,
        # it has uncounted fresh IDs
        if hi > max_hi:
            # Find lowest uncounted ID
            uncounted_lo = max(max_hi + 1, lo)
            # Tally all IDs up to max
            num_fresh += hi - uncounted_lo + 1
            # Update max high end
            max_hi = hi
        # Otherwise, nothing to do

    # Print result
    print(f"Part 2: {num_fresh}")


# Run for each input
for case in CASES:
    solve(*case)
    print("=" * 64)
