from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv
from app.config import Config
from app.db import db
from app.routes import contacts_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    Swagger(app)
    app.register_blueprint(contacts_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)