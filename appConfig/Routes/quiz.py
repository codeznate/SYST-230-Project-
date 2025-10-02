# Quiz page for website

from flask import Blueprint, render_template, request

quiz_bp = Blueprint("quiz", __name__, template_folder="templates")

@quiz_bp.route("/", methods = ["GET", "POST"])

def start_quiz():
    if request.method == "POST":
        answers = [request.form.get(f"q{i}") for i in range(1, 11)]

        score = 0
        for answer in answers:
            if answer == "strongly":
                score += 4
            elif answer == "agree":
                score += 3
            elif answer == "disagree":
                score += 2
            else:
                score += 1

        if score >= 37:
            suggested_major = "Engineering"
        elif score >= 34:
            suggested_major = "Computer Science"
        elif score >= 31:
            suggested_major = "Performing/Visual Arts"
        elif score >= 28:
            suggested_major = "Music Arts"
        elif score >= 25: 
            suggested_major = "Education"
        elif score >= 21:
            suggested_major = "Health Sciences"
        elif score >= 18:
            suggested_major = "Business"
        elif score >= 15:
            suggested_major = "Economics"
        else:
            suggested_major = "Entrepreneurship"
        return render_template("results.html", major = suggested_major)
    return render_template("quiz.html")