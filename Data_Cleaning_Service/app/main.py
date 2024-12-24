from Data_Cleaning_Service.app.db.postgres_db.database import create_tables, create_db
from Data_Cleaning_Service.app.services.process_csv import process_csv
from Data_Cleaning_Service.app.settings.kafka_settings.init_topics import init_topics

if __name__ == '__main__':
    create_db()
    init_topics()
    # process_csv("merged_terrorism_big_data.csv")
    process_csv("test.csv")


