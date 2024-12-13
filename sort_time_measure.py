import random
import timeit
import statistics
import csv

# optional for plotting (figures already included)
import matplotlib.pyplot as plt

from sorting_algorithms import sorting


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

    local_globals = globals().copy()
    local_globals["array"] = array

    repeat_times = timeit.repeat(
        stmt=algorithm_stmt, globals=local_globals, number=1, repeat=n_repeats
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
