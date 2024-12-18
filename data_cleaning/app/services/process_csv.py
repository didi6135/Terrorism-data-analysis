import os
import time

import pandas as pd

from data_cleaning.app.db.config import CLEANED_DATA_PATH
from data_cleaning.app.utils.logger import log
from data_cleaning.app.utils.split_to_models import main_split


def process_csv(file_name):
    """
    Processes a cleaned CSV file row by row and inserts into the database.
    """
    try:
        # Construct the full file path
        file_path = os.path.join(CLEANED_DATA_PATH, file_name)
        log(f"Starting to process CSV: {file_path}")

        # Load CSV data
        data = pd.read_csv(file_path, encoding='iso-8859-1')
        log(f"Loaded {len(data)} rows from {file_path}")

        # Process each row
        for index, row in data.iterrows():
            try:
                main_split(row)
                log(f"Processed row {index + 1} successfully.")
                time.sleep(1)
            except Exception as e:
                log(f"Error processing row {index + 1}: {e}", level="error")
                continue  # Skip to the next row if there's an error

        log(f"Finished processing CSV: {file_path}")

    except FileNotFoundError as e:
        log(f"File not found: {e}", level="error")
    except Exception as e:
        log(f"Error reading CSV file {file_name}: {e}", level="error")



