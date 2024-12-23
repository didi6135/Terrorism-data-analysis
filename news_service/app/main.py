import threading
import time
from threading import Thread

import schedule
from flask import Flask, current_app
from flask_cors import CORS

from news_service.app.db.elastic_search_db import create_index, news_mapping
from news_service.app.route.init_route import init_route
from news_service.app.route.news_route import news_routes
from news_service.app.settings.elastic_consumer import get_event_from_data_cleaning_consumer
from news_service.app.utils.scheduler import fetch_and_process_news


def run_scheduler():
    """
    Run the scheduler in a separate thread.
    """
    print("Starting scheduler...")
    fetch_and_process_news()  # Run once immediately on start
    while True:
        schedule.run_pending()
        time.sleep(1)


app = Flask(__name__, template_folder='templates')
CORS(app)
app.register_blueprint(news_routes, url_prefix="/news")
app.register_blueprint(init_route)



if __name__ == "__main__":
    create_index(index_name="news_articles", mapping=news_mapping)
    # scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    # scheduler_thread.start()
    # Start the Flask app
    Thread(name='consumer_for_new_events', target=get_event_from_data_cleaning_consumer).start()
    app.run(debug=True, host="0.0.0.0", port=5005)
