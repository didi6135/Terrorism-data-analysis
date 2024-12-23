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

    # res = count_unique_values_from_csv('data/cleaned/merged_terrorism_big_data.csv', 'gname')
    # print(res)
    # data = pd.read_csv('data/cleaned/test.csv').to_dict(orient="records")
    # print(data)
    # main_split(data)
    # with session_maker() as session:
    #     bulk_insert_all(data, session)

    # process_csv_batch("merged_terrorism_big_data.csv")

