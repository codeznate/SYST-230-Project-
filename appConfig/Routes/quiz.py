# Quiz page for website

from flask import Blueprint, render_template, request

quiz_bp = Blueprint("quiz", __name__, template_folder="templates")

@quiz_bp.route("/", methods = ["GET", "POST"])

def start_quiz():
    if request.method == "POST":
        answers = request.form
        suggested_career = "Computer Science" if answers.get("q1") == "Technology" else "Art"
        return render_template("results.html", career=suggested_career)
    return render_template("quiz.html")