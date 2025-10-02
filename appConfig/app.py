"""
This code sets up a basic Flask web application using the application factory pattern.

Imports: It imports Flask and three blueprints (home_bp, quiz_bp, majorSelect_bp) from separate route modules. 
Blueprints help organize routes and logic into reusable components.

create_app Function: This function creates a Flask app instance and registers the three blueprints:
    home_bp for the home page (no URL prefix).
    quiz_bp for quiz-related routes (with /quiz prefix).
    majorSelect_bp for major selection routes (with /decided prefix).

Main Block: If the script is run directly, it creates the app and starts the development server with debugging enabled.
Overall Function:
This file is the entry point for a Flask web app that organizes its routes using blueprints. It allows users to access different parts of the site (home, quiz, major selection) via modular route handlers. The app is started in debug mode for easier development and troubleshooting.
"""

from flask import Flask
from Routes.home import home_bp
from Routes.quiz import quiz_bp
from Routes.majorSelect import majorSelect_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    app.register_blueprint(quiz_bp, url_prefix = "/quiz")
    app.register_blueprint(majorSelect_bp, url_prefix = "/decided")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)