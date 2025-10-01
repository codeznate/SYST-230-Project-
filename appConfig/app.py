#Central app blueprint

from flask import Flask
from Routes.home import home_bp
from Routes.quiz import quiz_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    app.register_blueprint(quiz_bp, url_prefix = "/quiz")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)