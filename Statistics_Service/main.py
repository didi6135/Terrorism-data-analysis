from flask import Flask
from flask_cors import CORS

from Statistics_Service.app.routes.init_route import init_route
from Statistics_Service.app.routes.statistics import statistics_bp

app = Flask(__name__, template_folder='app/templates')
CORS(app)
app.register_blueprint(statistics_bp, url_prefix="/api/statistics")
app.register_blueprint(init_route)


if __name__ == "__main__":
    app.run(debug=True)