from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importamos y registramos el Blueprint del chatbot
    from app.main import chat
    app.register_blueprint(chat, url_prefix='/chat')

    return app
