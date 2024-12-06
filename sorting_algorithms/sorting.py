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


def merge_sort(data):

    # check if input data have more than one element
    size = len(data)
    if size > 1:

        # splitting part
        ############################

        # copy the input data
        array = data.copy()

        # find middle pint and divide the array into two halves
        mid = size // 2
        left_half = array[:mid]
        right_half = array[mid:]

        # recursively sort the two halves
        merge_sort(left_half)
        merge_sort(right_half)

        # merging part
        ############################

        # set initial index for left, right and merged arrays
        i = j = k = 0

        # start merging until one of the halves is empty
        while i < len(left_half) and j < len(right_half):

            # compare two elements and place the smaller one in the merged array
            # go through the halves
            if left_half[i] < right_half[j]:
                array[k] = left_half[i]
                i += 1
            else:
                array[k] = right_half[j]
                j += 1

        # one of the halves is empty, so place the remaining elements in the merged array
        while i < len(left_half):
            array[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            array[k] = right_half[j]
            j += 1
            k += 1

        return array
