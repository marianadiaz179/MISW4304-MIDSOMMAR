from dotenv import load_dotenv
from flask import Flask
from api.src.routes.blacklist_router import blacklist_bp
from api.src.config.config import Config
from api.src.models.models import db


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(blacklist_bp)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000)