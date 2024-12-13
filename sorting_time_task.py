"""
Time measuring of sorting algorithms
"""

# sorting algorithms test - correct results

from sorting_algorithms import sorting

data = [-2, 45, 0, 11, -9]
array = [6, 5, 12, 10, 9, 1]

assert sorting.selection_sort(data) == [-9, -2, 0, 11, 45]
assert sorting.bubble_sort(data) == [-9, -2, 0, 11, 45]

print(sorting.merge_sort(array))

assert sorting.merge_sort(array) == [1, 5, 6, 9, 10, 12]

print("Sorting algorithms test passed")
