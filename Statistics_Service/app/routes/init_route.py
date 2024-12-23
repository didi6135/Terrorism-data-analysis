from flask import render_template, Blueprint

init_route = Blueprint('init_route', __name__)

@init_route.route("/")
def home():
    return render_template("index.html")