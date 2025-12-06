from functools import reduce
from pathlib import Path

CASES = [("../inputs/day6_example.txt",), ("../inputs/day6.txt",)]


def solve(input_path: str | Path):
    input_path = Path(input_path)
    print(f"Solving {input_path.stem}")

    # Open input file and read all lines
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # PART 1
    # Create 2D grid of operands matching the shape in the input
    # (each column contains the operands for one problem)
    operands_grid = [[int(num) for num in line.rstrip().split()] for line in lines[:-1]]
    # List of operators
    operators = lines[-1].split()

    num_problems = len(operators)
    print(f"{num_problems} problems")

    # Compute the total:
    grand_total = 0

    # For each problem (operator),
    for i, operator in enumerate(operators):
        # Get generator for the corresponding column of operands
        operands = (operand_row[i] for operand_row in operands_grid)
        # Compute answer based on operand
        if operator == "+":
            answer = sum(operands)
        else:
            answer = reduce(lambda acc, x: acc * x, operands)
        # Add to total
        grand_total += answer

    # Print result
    print(f"Part 1: {grand_total}")

    # PART 2
    # Parse the input differently...
    # Read column by column, matching the digit alignment,
    # obtaining an operand each column
    # A column of nothing indicates the end of a problem

    # List of operators
    operators = lines[-1].split()
    num_problems = len(operators)

    col = 0  # Current column in input being read
    operands_grid = []  # Grid is rotated from Part 1; each row contains operands for one problem
    # For each problem (operator)...
    for _ in range(num_problems):
        # Create a list for the operands
        problem_operands = []

        # Loop until blank column
        while True:
            # Get chars in the column. If out of range for a row, use " " as placeholder
            chars = [
                line[col] if col < len(line.rstrip()) else " " for line in lines[:-1]
            ]
            # Increment col to read next
            col += 1

            # If all spaces, reached end of problem
            if all(c == " " for c in chars):
                break

            # Get operand by joining digits in column
            operand = "".join(filter(lambda c: c != " ", chars))
            operand = int(operand)
            # Add to list
            problem_operands.append(operand)

        # Add operand list to list
        operands_grid.append(problem_operands)

    # Computing the total is now straightforward:
    grand_total = 0
    # For each problem (operator)...
    for i, operator in enumerate(operators):
        # Compute answer based on operand
        if operator == "+":
            answer = sum(operands_grid[i])
        else:
            answer = reduce(lambda acc, x: acc * x, operands_grid[i])
        # Add to total
        grand_total += answer

    # Print result
    print(f"Part 2: {grand_total}")


# Run for each input
for case in CASES:
    solve(*case)
    print("=" * 64)
