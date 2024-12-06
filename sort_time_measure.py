import random
import timeit
import time
import statistics
import matplotlib.pyplot as plt
import csv

ARRAY_SIZE = [100, 200, 500, 1000, 2000, 5000, 10000]
ALGORITHMS = ["Selection", "Bubble", "Merge", "Sorted()"]

sorting_algorithms = {
    "Selection": "selection_sort(array.copy())",
    "Bubble": "bubble_sort(array.copy())",
    "Merge": "merge_sort(array.copy())",
    "Sorted()": "sorted(array.copy())",
}


def measure_time(
    algorithm, array_length, number_range_min, number_range_max, repeat_times
):
    array = [
        random.randint(number_range_min, number_range_max) for _ in range(array_length)
    ]
    stmt = sorting_algorithms[algorithm]
    repeat_times = timeit.repeat(
        stmt=stmt, globals=globals(), number=1, repeat=repeat_times
    )
    mean_time = statistics.mean(repeat_times)
    std_dev_time = statistics.stdev(repeat_times)
    with open("sorting_time.csv", "a", encoding="utf-8") as f:
        row = [algorithm, array_length, mean_time, std_dev_time, repeat_times]
        f.write(",".join(map(str, row)) + "\n")

    return mean_time, std_dev_time


def compare_algorithms(
    algoritms,
    length_of_arrays,
    number_range_min=0,
    number_range_max=1000,
    repeat_times=5,
):
    with open("sorting_time.csv", "w", encoding="utf-8") as f:
        header = [
            "Algorithm",
            "Array Size",
            "Mean",
            "Standard Deviation",
            "Number of repeats",
        ]
        f.write(",".join(header) + "\n")

    for algorithm in algoritms:
        for array_length in length_of_arrays:
            mean_time, std_dev_time = measure_time(
                algorithm,
                array_length,
                number_range_min,
                number_range_max,
                repeat_times,
            )
            print(
                f"Algorithm: {algorithm}, Array size: {array_length}, Mean time: {mean_time}, Standard deviation: {std_dev_time}"
            )


def plot_algorithm_comparison():
    times = {}
    with open("sorting_time.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["Algorithm"]
            n = int(row["Array Size"])
            mean_time = float(row["Mean"])
            std_dev_time = float(row["Standard Deviation"])

            if name not in times:
                times[name] = {"sizes": [], "means": [], "std_devs": []}
            times[name]["sizes"].append(n)
            times[name]["means"].append(mean_time)
            times[name]["std_devs"].append(std_dev_time)

    plt.figure(figsize=(12, 8))

    for name, data in times.items():
        sizes = data["sizes"]
        means = data["means"]
        std_devs = data["std_devs"]
        lower_bound = [mean - std_dev for mean, std_dev in zip(means, std_devs)]
        upper_bound = [mean + std_dev for mean, std_dev in zip(means, std_devs)]

        (mean_line,) = plt.plot(sizes, means, label=f"{name} (mean)")
        color = mean_line.get_color()

        plt.plot(
            sizes,
            lower_bound,
            linestyle="--",
            color=color,
            label=f"{name} (mean - std_dev)",
        )
        plt.plot(
            sizes,
            upper_bound,
            linestyle="--",
            color=color,
            label=f"{name} (mean + std_dev)",
        )

    plt.xlabel("Array Size")
    plt.ylabel("Time [seconds]")
    plt.title("Sorting Algorithm Performance")
    plt.legend()
    plt.grid(True)
    plt.savefig("sorting_performance.png")
    plt.show()


"""
Sorting algorithms
"""

import time


# decorator for time measuring
def calculate_time(func):

    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        stop = time.time()

        print(f"{func.__name__} elapsed time: { stop - start } s")
        return result

    return inner


# @calculate_time
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


# @calculate_time
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


if __name__ == "__main__":
    # compare_algorithms(ALGORITHMS, ARRAY_SIZE)
    plot_algorithm_comparison()
    plt.show()
