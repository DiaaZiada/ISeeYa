from flask import  url_for, redirect, Blueprint

main = Blueprint('main', __name__)


@main.route("/")
def home():
    return redirect(url_for('pages.page', page_name="home"))
