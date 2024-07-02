import os
from flask import render_template
from app import create_app

app = create_app()

@app.route('/')
def home():
    
    try:
        print("Current working directory:", os.getcwd())
        print("Template directory contents:", os.listdir('templates'))
        app.template_folder = os.path.join(os.getcwd(), 'templates')
        return render_template('index.html')
    except Exception as e:
        print("Error rendering template:", str(e))
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
