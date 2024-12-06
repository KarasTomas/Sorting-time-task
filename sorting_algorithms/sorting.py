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


def bubble_sort(data):

    # copy the input data
    array = data.copy()
    size = len(array)

    # iterate through the whole list / array
    for pass_length in range(size):

        # track of swapping
        swapped = False

        # iterate to compare elements in list / array
        for element in range(size - pass_length - 1):

            # compare two adjacent elements
            # change order from ascending to descending by changing the sign
            if array[element] > array[element + 1]:

                # swap the elements
                (array[element], array[element + 1]) = (
                    array[element + 1],
                    array[element],
                )

                # track the swap
                swapped = True

        # no swapping means the array is already sorted
        # so no need for further comparison
        if not swapped:
            break

    return array
