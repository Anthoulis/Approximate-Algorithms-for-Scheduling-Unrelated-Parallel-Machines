import csv
import random
import shutil


def generate_random_value():
    # r_number = random.random()
    # if r_number < 0.9:
    #     return random.randint(4, 7)
    # else:
    #     if r_number < 0.95:
    #         return random.randint(1, 3)
    #     return random.randint(8, 10)
    return random.randint(1, 100)


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
    write_csv_file("random_data.csv", data_array)

    # Print data
    # CSV_functions.print_csv_file_data(data_array)


def save_to_data():
    source_file = "random_data.csv"
    destination_file = "data.csv"

    # Copy the source file to the destination file
    shutil.copyfile(source_file, destination_file)


# --------------   CSV Functions -------------------------------------------------
def read_csv_file(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append([int(cell) for cell in row])
    return data


def write_csv_file(filename, data):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)


def print_csv_file_data(data):
    for row in data:
        print(row)
