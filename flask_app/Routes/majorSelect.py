#Page if decided is clicked

from flask import Blueprint, render_template 

majorSelect_bp = Blueprint("majorSelect", __name__)

@majorSelect_bp.route("/")
def majorSelect():
    return render_template("majorSelect.html")
