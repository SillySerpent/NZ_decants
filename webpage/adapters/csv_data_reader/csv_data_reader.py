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

            for row in csv_reader:
                if len(row) != 16:  # Adjust the expected column count if needed
                    print(f"Skipping malformed row: {row}")
                    continue
                yield [item.strip() for item in row]

    def create_cologne(self, row):
        try:
            price = float(row[0])
            name = str(row[1])
            size = int(row[2])
            picture_url = str(row[3])
            description = str(row[4])
            id = int(row[5])
            season = str(row[6])
            category = str(row[7])
            sex = row[8].split(",")  # Assuming this is a list
            discount = float(row[9])
            featured = row[10].strip().lower() == "true"
            availability = row[11].strip().lower() == "true"
            rating = int(row[12])
            notes = row[13]  # Assuming this is a list
            release_year = int(row[14])
            concentration = str(row[15])

            return Cologne(
                id=id, price=price, name=name, size=size, picture_url=picture_url,
                description=description, season=season, category=category,
                sex=sex, discount=discount, featured=featured,
                availability=availability, rating=rating, notes=notes,
                release_year=release_year, concentration=concentration
            )
        except ValueError as e:
            print(f"Error parsing row: {row}, error: {e}")
            return None

    def populate_db_temp(self):
        for row in self.read_csv():
            cologne = self.create_cologne(row)
            if cologne:  # Only add if the Cologne object is created successfully
                self.temp_storage.append(cologne)


    def populate_db(self, app):
        """Populate the database with cologne data."""
        with app.app_context():  # Make sure to use the app context
            for row in self.read_csv():
                cologne = self.create_cologne(row)
                if cologne:
                    self.db.session.add(cologne)
            self.db.session.commit()  # Commit the changes to the database








