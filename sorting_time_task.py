"""
Time measuring of sorting algorithms

Size of lists and number of repeats are lowered for testing purposes

"""

import random

import sort_time_measure as tm

# Selection of sorting algorithms
sorting_algorithms = {
    "Selection": "sorting.selection_sort(array.copy())",
    "Bubble": "sorting.bubble_sort(array.copy())",
    "Merge": "sorting.merge_sort(array.copy())",
    "Sorted()": "sorted(array.copy())",
}

# Lengths of arrays to sort
lengths = [100, 200, 500, 1_000]

# Prepare CSV file, this can be commented out if you just want to add more data
tm.prepare_csv_file()

# Loop through array lengths and compare sorting algorithms
for array_size in lengths:
    array = [random.randint(-1000, 1000) for _ in range(array_size)]
    tm.compare_algorithms(sorting_algorithms, array, n_repeats=2)

# Plot the comparison
tm.plot_algorithm_comparison()
