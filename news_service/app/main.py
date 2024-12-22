import threading
import time

import schedule
from flask import Flask

from news_service.app.db.elastic_search_db import create_index, news_mapping, index_name
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

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)
    app.register_blueprint(news_routes, url_prefix="/news")
    return app

if __name__ == "__main__":
    # Start the scheduler in a separate thread
    create_index(index_name, news_mapping)
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Start the Flask app
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
