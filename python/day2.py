from pathlib import Path

CASES = [("../inputs/day2_example.txt",), ("../inputs/day2.txt",)]


def solve(input_path: str | Path):
    input_path = Path(input_path)
    print(f"Solving {input_path.stem}")

    # Open input file and read the single line
    with open(input_path, "r", encoding="utf-8") as file:
        input_str = file.read()

    # Split into pairs of first and last ID of ranges
    ranges = [
        [int(id) for id in id_range.split("-")] for id_range in input_str.split(",")
    ]

    # PART 1
    sum = 0

    # Use the basic method of checking every number.
    # For each range...
    for id_range in ranges:
        # Get the min, max
        range_min, range_max = id_range
        # For each ID in range...
        for id in range(range_min, range_max + 1):
            # Get the front and back halves of the digits
            id_str = str(id)
            front, back = id_str[: len(id_str) // 2], id_str[len(id_str) // 2 :]
            # If they're equal, add ID to sum
            if front == back:
                sum += id

    # Print result
    print(f"Part 1: {sum}")

    # PART 2
    sum = 0

    # Continue with checking all numbers.
    # For each range...
    for id_range in ranges:
        # Get the min, max
        range_min, range_max = id_range
        # For each ID in range...
        for id in range(range_min, range_max + 1):
            # Get it as str, and get its len
            id_str = str(id)
            id_len = len(id_str)
            # For each possible sequence length, up to half of the ID len,
            for seq_len in range(1, id_len // 2 + 1):
                # If the ID len is a multiple of the seq len,
                if id_len % seq_len == 0:
                    # Check if the ID is equal to the seq repeated up to the full length
                    seq = id_str[:seq_len]
                    if seq * (id_len // seq_len) == id_str:
                        # If so, add ID to sum
                        sum += id
                        # Done with this ID, it can only be counted once
                        break

    # Print result
    print(f"Part 2: {sum}")


# Run for each input
for case in CASES:
    solve(*case)
    print("=" * 64)
