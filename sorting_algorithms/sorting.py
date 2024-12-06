"""
Sorting algorithms
"""


def selection_sort(data):

    # copy the input data
    array = data.copy()
    size = len(array)

    # iterate through the whole list / array
    for step in range(size):
        min_index = step

        # iterate from step index because the first elements are already sorted
        for i in range(step, size):

            # find the smallest element in current loop
            if array[i] < array[min_index]:
                min_index = i

        # swap the found smallest element with the first element of the current loop (correct position)
        (array[step], array[min_index]) = (array[min_index], array[step])
        # swap utilizing tuple packing and unpacking -> does not need a temporary variable

    return array
