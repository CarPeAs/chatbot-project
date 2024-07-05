from flask import Flask, render_template
import os

def create_app():
    # Configuramos las rutas correctas para las carpetas estáticas y de plantillas
    app = Flask(
        __name__,
        static_url_path='/static',
        static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static'),
        template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
    )

    @app.route('/')
    def home():
        return render_template('index.html')
    
    # Importamos y registramos el Blueprint del chatbot
    from app.main import chat
    app.register_blueprint(chat, url_prefix='/chat')

    return app

