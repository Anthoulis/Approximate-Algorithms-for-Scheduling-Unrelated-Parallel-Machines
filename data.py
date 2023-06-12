import random
import shutil

import CSV_functions


def generate_random_value():
    r_number = random.random()
    if r_number < 0.9:
        return random.randint(4, 7)
    else:
        if r_number < 0.95:
            return random.randint(1, 3)
        return random.randint(8, 10)


def generate_random_data(m, n):
    Pij = []

    for _ in range(m):
        machine_times = [generate_random_value() for _ in range(n)]
        Pij.append(machine_times)

    return Pij


def run_data():
    m = 100
    n = 200
    data_array = generate_random_data(m, n)

    # Write data to CSV file
    CSV_functions.write_csv_file("random_data.csv", data_array)

    # Print data
    CSV_functions.print_csv_file_data(data_array)


def save_to_data():
    source_file = "random_data.csv"
    destination_file = "data.csv"

    # Copy the source file to the destination file
    shutil.copyfile(source_file, destination_file)


if __name__ == "__main__":
    run_data()
