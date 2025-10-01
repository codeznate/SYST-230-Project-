# Quiz page for website

from flask import Blueprint, render_template, request

quiz_bp = Blueprint("quiz", __name__, template_folder="templates")

@quiz_bp.route("/", methods = ["GET", "POST"])

def start_quiz():
    if request.method == "POST":
        answer = request.form.get("q1")
        if answer == "strongly" or answer == "agree":
            suggested_career = "Engineering"
        elif answer == "disagree":
            suggested_career = "Arts"
        else:
            suggested_career = "Computer science"
        return render_template("results.html", major=suggested_career)
    return render_template("quiz.html")