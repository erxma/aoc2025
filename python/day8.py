import heapq
import math
from functools import reduce
from itertools import combinations
from pathlib import Path

CASES = [("../inputs/day8_example.txt", 10), ("../inputs/day8.txt", 1000)]


# Basic impl of a union-find using indices as nodes,
# without optimizations, tracking tree sizes and the number of sets
class UnionFind:
    def __init__(self, size):
        # Lookup by indexing array with node ID
        self.parents = list(range(size))  # Immediate parent of each node
        self.sizes = [1] * size  # Size of the (sub)tree rooted at each node
        self.num_sets = size  # Number of disjoint sets remaining

    def find(self, i):
        if self.parents[i] == i:
            return i
        return self.find(self.parents[i])

    def union(self, a, b):
        # Find roots ("representatives") of the two nodes
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a != root_b:
            # Attach root of smaller tree to root of larger
            # and update size
            if self.sizes[root_a] < self.sizes[root_b]:
                self.parents[root_a] = root_b
                self.sizes[root_b] += self.sizes[root_a]
            else:
                self.parents[root_b] = root_a
                self.sizes[root_a] += self.sizes[root_b]
            # A union occurred, so there's one set fewer
            self.num_sets -= 1


def solve(input_path: str | Path, connections: int):
    input_path = Path(input_path)
    print(f"Solving {input_path.stem}")

    # Open input file and read all lines
    with open(input_path, "r", encoding="utf-8") as file:
        input_txt = file.readlines()

    # Split into list of 3 coords for each box
    boxes = [[int(coord) for coord in line.rstrip().split(",")] for line in input_txt]

    num_boxes = len(boxes)
    print(f"Input contains {num_boxes} boxes")

    # Use naive method of computing distance between all pairs
    # Make list of (distance, box index 1, box index 2)
    pair_distances = [
        (math.dist(boxes[i1], boxes[i2]), i1, i2)
        for i1, i2 in combinations(range(num_boxes), 2)
    ]

    # PART 1

    # Make copy of pair distances to mutate
    # Convert to min-heap
    # (Since distance is first in the tuples, it's used as key)
    pairs_heap = pair_distances.copy()
    heapq.heapify(pairs_heap)

    # Create union-find of boxes, represented by index in boxes
    union_find = UnionFind(len(boxes))

    # For specified number of times, pop closest pair and union them
    for _ in range(connections):
        _, i1, i2 = heapq.heappop(pairs_heap)
        union_find.union(i1, i2)

    # Get circuit sizes, which are the tree sizes for boxes that are roots
    circuit_sizes = [
        size for i, size in enumerate(union_find.sizes) if union_find.parents[i] == i
    ]

    # Just sort it all and take top 3
    top_3 = sorted(circuit_sizes, reverse=True)[:3]
    # Multiply them
    result = reduce(lambda acc, x: acc * x, top_3)

    # Print result
    print(f"Part 1: Top 3 are {top_3}, for product of {result}")

    # PART 2

    # Using union-find, keep connecting until a root hits size
    # equal to the number of boxes, last pair to be connected is the target

    # Make new copy of pair distances and union-find
    pairs_heap = pair_distances.copy()
    heapq.heapify(pairs_heap)
    union_find = UnionFind(len(boxes))

    # Keep connecting boxes until...
    while True:
        _, i1, i2 = heapq.heappop(pairs_heap)
        union_find.union(i1, i2)
        # ...until the number of disjoint sets hits 1,
        # i.e. everything's in one circuit
        if union_find.num_sets == 1:
            break

    # Get result based on last two boxes to be connected
    result = boxes[i1][0] * boxes[i2][0]

    # Print result
    print(f"Part 2: Last pair is {boxes[i1]}, {boxes[i2]}, for product of {result}")


# Run for each input
for case in CASES:
    solve(*case)
    print("=" * 64)
