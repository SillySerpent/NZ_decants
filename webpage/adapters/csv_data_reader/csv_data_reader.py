import csv


def read_csv(file_pathway: str):
    with open(file_pathway) as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)

        for row in csv_reader:
            row = [item.strip() for item in row]
            yield row


class CsvDataReader:

    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path


