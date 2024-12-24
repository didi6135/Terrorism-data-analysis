from Data_Cleaning_Service.app.db.postgres_db.database import session_maker, create_tables
from Data_Cleaning_Service.app.services.process_csv import process_csv
import pandas as pd

from Data_Cleaning_Service.app.services.split_to_postgres import main_split
from Data_Cleaning_Service.app.settings.kafka_settings.init_topics import init_topics

if __name__ == '__main__':
    # create_tables()
    init_topics()
    # process_csv("test.csv")
    process_csv("merged_terrorism_big_data.csv")



