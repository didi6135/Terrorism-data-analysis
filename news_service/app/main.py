import time
from threading import Thread

import schedule
from flask import Flask
from flask_cors import CORS

from news_service.app.db.elastic_search_db import create_index, news_mapping
from news_service.app.route.init_route import init_route
from news_service.app.route.news_route import news_routes
from news_service.app.settings.elastic_consumer import get_event_from_data_cleaning_consumer
from news_service.app.utils.scheduler import fetch_and_process_news


def run_scheduler():
    while True:
        print("Starting the news fetching scheduler...")
        fetch_and_process_news()
        time.sleep(50)


def start_consumer():
    print("Starting the consumer for new events...")
    get_event_from_data_cleaning_consumer()


app = Flask(__name__, template_folder="templates")
CORS(app)
app.register_blueprint(news_routes, url_prefix="/news")
app.register_blueprint(init_route)


if __name__ == "__main__":
    # Create index for Elasticsearch
    create_index(index_name="news_articles", mapping=news_mapping)

    # Start background threads for scheduler and consumer
    scheduler_thread = Thread(target=run_scheduler, name="SchedulerThread", daemon=True)
    consumer_thread = Thread(target=start_consumer, name="ConsumerThread", daemon=True)

    scheduler_thread.start()
    consumer_thread.start()
    app.run(debug=True, host="localhost", port=5005)

    # Run the Flask app
