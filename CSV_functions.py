import csv


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


if __name__ == "__main__":
    print('Testing CSV_functions.py')
    # Add code for testing
