import threading
import time

import schedule
from flask import Flask, current_app
from flask_cors import CORS

from news_service.app.db.elastic_search_db import create_index, news_mapping, index_name
from news_service.app.route.init_route import init_route
from news_service.app.route.news_route import news_routes
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

    # Start the scheduler in a separate thread
    # scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    # scheduler_thread.start()
    # Start the Flask app
    app.run(debug=True, host="0.0.0.0", port=5005)
