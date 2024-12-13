import random
import timeit
import time
import statistics
import csv

# optional for plotting (figures already included)
import matplotlib.pyplot as plt


def measure_time(
    algorithm: str, algorithm_stmt: str, array: list[int], n_repeats: int
) -> tuple[float, float]:
    """
    Function for measuring time of the algorithm.

    Args:
        algorithm (str): Name of the algorithm.
        algorithm_stmt (str): Statement of the algorithm (algorithm code).
        array (list[int]): Array to sort.
        n_repeats (int): Number of test repeats.

    Returns:
        mean_time (float): Mean time of the algorithm.
        std_dev_time (float): Standard deviation of the algorithm.

    """

    repeat_times = timeit.repeat(
        stmt=algorithm_stmt, globals=globals(), number=1, repeat=n_repeats
    )

    mean_time = statistics.mean(repeat_times)
    std_dev_time = statistics.stdev(repeat_times)

    _save_measured_time(
        "sorting_time.csv", algorithm, len(array), mean_time, std_dev_time, n_repeats
    )

    return mean_time, std_dev_time


def _save_measured_time(
    file_name: str,
    algorithm: str,
    array_size: int,
    mean_time: float,
    std_dev_time: float,
    n_repeats: int,
) -> None:
    """
    Save measured time to a CSV file.

    Args:
        file_name (str): Name of the CSV file.
        algorithm (str): Name of the algorithm.
        array_size (int): Size of the array.
        mean_time (float): Mean time of the algorithm.
        std_dev_time (float): Standard deviation of the algorithm.
        n_repeats (int): Number of test repeats.

    Returns:
        None

    """
    if not file_name.endswith(".csv"):
        file_name += ".csv"

    with open(file_name, "a", encoding="utf-8") as f:
        row = [algorithm, array_size, mean_time, std_dev_time, n_repeats]
        f.write(",".join(map(str, row)) + "\n")


def compare_algorithms(
    algorithms: dict[str, str],
    array: list[int],
    n_repeats: int = 100,
) -> None:
    """
    Function for comparing selected algorithms.

    Args:
        algorithms (dict[str, str]): Dictionary with algorithm names and statements.
        array (list[int]): Array to sort.
        n_repeats (int): Number of test repeats.

    Returns:
        None

    """
    for algorithm, stmt in algorithms.items():
        mean_time, std_dev_time = measure_time(
            algorithm,
            stmt,
            array,
            n_repeats,
        )
        print(
            f"Algorithm: {algorithm}, Array size: {len(array)}, Mean time: {mean_time}, Standard deviation: {std_dev_time}"
        )


def prepare_csv_file(name: str = "sorting_time.csv") -> None:
    """
    Prepare CSV file for saving measured time. Write header to the file.

    Args:
        name (str): Name of the CSV file.

    Returns:
        None

    """
    with open(name, "w", encoding="utf-8") as f:
        header = [
            "Algorithm",
            "Array Size",
            "Mean",
            "Standard Deviation",
            "Number of repeats",
        ]
        f.write(",".join(header) + "\n")


def plot_algorithm_comparison(name: str = "sorting_time.csv") -> None:
    """
    Function for plotting the comparison of sorting algorithms. Reads data from the CSV file. Saves the plot as a PNG file.

    Args:
        name (str): Name of the CSV file.

    Returns:
        None
    """

    times = {}
    with open(name, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["Algorithm"]
            n = int(row["Array Size"])
            mean_time = float(row["Mean"])
            std_dev_time = float(row["Standard Deviation"])
            n_repeats = int(row["Number of repeats"])

            if name not in times:
                times[name] = {"sizes": [], "means": [], "std_devs": []}
            times[name]["sizes"].append(n)
            times[name]["means"].append(mean_time)
            times[name]["std_devs"].append(std_dev_time)
            times[name]["n_repeats"] = n_repeats

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


def merge_sort(array):

    # check if input data have more than one element

    if len(array) > 1:

        # splitting part
        ############################

        # find middle pint and divide the array into two halves
        mid = len(array) // 2
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

            k += 1

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

    # sorting algorithms test
    test_array = [random.randint(-100, 100) for _ in range(10)]
    correctly_sorted = sorted(test_array)

    # selection sort
    assert selection_sort(test_array) == correctly_sorted

    # bubble sort
    assert bubble_sort(test_array) == correctly_sorted

    # merge sort
    assert merge_sort(test_array) == correctly_sorted

    sorting_algorithms = {
        "Selection": "selection_sort(array.copy())",
        "Bubble": "bubble_sort(array.copy())",
        "Merge": "merge_sort(array.copy())",
        "Sorted()": "sorted(array.copy())",
    }

    lengths = [100, 200, 500, 1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000]

    prepare_csv_file()

    for array_size in lengths:
        array = [random.randint(-1000, 1000) for _ in range(array_size)]
        compare_algorithms(sorting_algorithms, array, n_repeats=100)

    plot_algorithm_comparison()
