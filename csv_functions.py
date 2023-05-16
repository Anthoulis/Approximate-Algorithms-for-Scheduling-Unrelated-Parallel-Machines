import csv


def set_initial_deadlines(pij, factor=1.5):
    """
    Set the initial deadlines based on the maximum processing time in the data.

    Args:
        pij (list of lists): Processing times of jobs on machines.
        factor (float): A factor to multiply with the maximum processing time to determine the initial deadline.
                        Default value is 1.5.

    Returns:
        list: Initial deadlines for each machine.
    """
    max_processing_time = max(max(pij[i]) for i in range(len(pij)))
    initial_deadlines = [factor * max_processing_time] * len(pij)
    return initial_deadlines


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
