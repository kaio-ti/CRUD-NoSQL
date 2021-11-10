from flask import Flask

def create_app():

    app = Flask(__name__)

    from app.controller import controller

    controller.init_app(app)

    return app

    