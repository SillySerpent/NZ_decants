import csv
from webpage.domain_model.domain_model import Cologne
from pathlib import Path


class CsvDataReader:
    temp_storage = []

    def __init__(self, db, csv_file_path=None):
        self.db = db
        base_dir = Path(__file__).resolve().parent.parent.parent
        self.csv_file_path = base_dir / "adapters" / "data" / "cologne_data.csv"
        self.temp_storage = []  # Initialize as an empty list

    def read_csv(self):
        with open(self.csv_file_path, newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            for i, row in enumerate(csv_reader, start=1):
                if len(row) != 11:  # Adjust the expected column count if needed
                    print(f"Skipping malformed row {i}: {row}")
                    continue
                yield [item.strip() for item in row]

    def create_cologne(self, row):
        try:
            price = float(row[0])
            name = str(row[1])
            size = int(row[2])
            picture_url = str(row[3])
            description = str(row[4])
            season = str(row[5])
            sex = row[6]  # Assuming this is a list
            rating = int(row[7])
            notes = row[8]  # Assuming this is a list
            release_year = int(row[9])
            concentration = str(row[10])

            return Cologne(
                price=price, name=name, size=size, picture_url=picture_url,
                description=description, season=season, sex=sex,
                rating=rating, notes=notes, release_year=release_year,
                concentration=concentration
            )

        except ValueError as e:
            print(f"Error parsing row: {row}, error: {e}")
            return None

    def populate_db_temp(self):
        for row in self.read_csv():
            cologne = self.create_cologne(row)
            if cologne:  # Only add if the Cologne object is created successfully
                self.temp_storage.append(cologne)

    def populate_db(self):
        rows = (self.create_cologne(row) for row in self.read_csv())
        colognes = [c for c in rows if c is not None]
        self.db.session.bulk_save_objects(colognes)
        self.db.session.commit()
