import csv
import os
import random


def generate_random_value():
    """
    The way and the range where values are generated
    :return: The processing time of a job are between 1-100
    """
    return random.randint(1, 100)


def generate_pij(m, n):
    """
    Fill the 2d array Pij according to generate_random_value
    :param m: number of machines
    :param n: number of jobs
    :return: 2d array Pij
    """
    Pij = []

    for _ in range(m):
        machine_times = [generate_random_value() for _ in range(n)]
        Pij.append(machine_times)

    return Pij


def generate_filedata(filename: [], m: int, n: int):
    """
    If the file exists, it reads it and returns its data
    Else it creates a new file and generates data
    :param filename: Name of the file
    :param m: Number of machine
    :param n: number of jobs
    :return: 2d array Pij
    """
    # Check if the file already exists
    if os.path.isfile(filename):
        # Read and save the data from the existing file
        data = read_csv_file(filename)
    else:
        data = generate_pij(m, n)
        write_data_to_csv(filename, data)
    return data


# --------------   CSV Functions -------------------------------------------------


def read_csv_file(filename):
    if os.path.isfile(filename):
        data = []
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append([int(cell) for cell in row])
        return data
    else:
        print("File not Found")
        return None


def write_data_to_csv(filename, data):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)


def print_csv_file(filename):
    # Check if the file already exists
    if os.path.isfile(filename):
        # Read and save the data from the existing file
        data = read_csv_file(filename)
        for row in data:
            print(row)
    else:
        print("File not found")


# Generate File Data
# generate_filedata("filename", m, n)
if __name__ == "__main__":
    generate_filedata("data3x10.csv", 3, 10)

