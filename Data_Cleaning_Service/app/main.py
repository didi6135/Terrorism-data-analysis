from Data_Cleaning_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.services.process_csv import process_csv
import pandas as pd

from Data_Cleaning_Service.app.services.split_to_postgres import bulk_insert_all


def count_unique_values_from_csv(file_path, column_name):
    """
    Reads a CSV file and counts the unique values in a specified column.

    :param file_path: str, path to the CSV file.
    :param column_name: str, the name of the column to analyze.
    :return: int, count of unique values in the specified column.
    """
    try:
        # Load the CSV file
        data = pd.read_csv(file_path)

        # Check if the column exists
        if column_name not in data.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the provided CSV file.")

        # Count unique values
        unique_count = data[column_name].nunique()

        return unique_count
    except Exception as e:
        print(f"Error while processing the file: {e}")
        return None




if __name__ == '__main__':
    # process_csv("test.csv")
    # process_csv("merged_terrorism_big_data.csv")
    data = pd.read_csv('data/cleaned/merged_terrorism_big_data.csv').to_dict(orient="records")

    with session_maker() as session:
        bulk_insert_all(data, session)
    # res = count_unique_values_from_csv('data/cleaned/merged_terrorism_big_data.csv', 'gname')
    # print(res)
    # process_csv_batch("merged_terrorism_big_data.csv")

