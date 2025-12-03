from pathlib import Path

CASES = [("../inputs/day3_example.txt",), ("../inputs/day3.txt",)]


def solve(input_path: str | Path):
    input_path = Path(input_path)
    print(f"Solving {input_path.stem}")

    # Open input file and read all lines
    with open(input_path, "r", encoding="utf-8") as file:
        banks = file.readlines()

    # Convert battery values to ints
    banks = [[int(joltage) for joltage in bank.rstrip()] for bank in banks]

    # PART 1
    max_total = 0

    for bank in banks:
        # Best tens place is always leftmost instance of max rating (except last in bank)
        tens_place = max(bank[:-1])
        tens_val_pos = bank.index(tens_place)

        # Then, the best ones place is the max rating after the tens place
        ones_place = max(bank[tens_val_pos + 1 :])

        # Compute the bank's joltage and add to total
        bank_joltage = tens_place * 10 + ones_place
        max_total += bank_joltage

    # Print result
    print(f"Part 1: {max_total}")

    # PART 2
    max_total = 0

    NUM_DIGITS = 12

    # Similar to Part 1, except repeat the process for 12 places.
    # This also means most significant digit must be at least 12 from the last, and so on
    for bank in banks:
        bank_joltage = 0
        val_pos = -1
        for digit in range(NUM_DIGITS):
            # Best value for place is always leftmost instance of max rating
            # between the last used digit and the last digit that'd leave enough afterwards
            left_bound = val_pos + 1
            right_bound = len(bank) - NUM_DIGITS + digit
            place_val = max(bank[left_bound : right_bound + 1])
            # Be careful to search within the correct range, and get the absolute index
            val_pos = bank[left_bound : right_bound + 1].index(place_val) + left_bound

            # Add digit to end of number
            bank_joltage = bank_joltage * 10 + place_val

        # Add to total
        max_total += bank_joltage

    # Print result
    print(f"Part 2: {max_total}")


# Run for each input
for case in CASES:
    solve(*case)
    print("=" * 64)
