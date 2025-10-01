# Quiz page for website

from flask import Blueprint, render_template 

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/", methods = ["GET", "POST"])

def start_quiz():
    return render_template("quiz.html")