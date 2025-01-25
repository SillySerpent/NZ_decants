from sqlalchemy.orm import scoped_session

from webpage import CsvDataReader
from webpage.domain_model.domain_model import Cologne


def populate_db(session_factory: scoped_session):
    data_reader = CsvDataReader(session_factory)

    try:
        session = session_factory()  # Get a session from the factory
        # Check if the Cologne table already has data
        if session.query(Cologne).first() is not None:
            print("Database already populated. Skipping population.")
            return

        print("Populating the database with data from the CSV file...")
        # Read rows from CSV and create Cologne objects
        rows = (data_reader.create_cologne(row) for row in data_reader.read_csv())
        colognes = [c for c in rows if c is not None]

        # Bulk save objects to the database
        session.bulk_save_objects(colognes)
        session.commit()
        print(f"{len(colognes)} colognes added to the database.")
    except Exception as e:
        session.rollback()
        print(f"Error populating the database: {e}")
    finally:
        session.close()
