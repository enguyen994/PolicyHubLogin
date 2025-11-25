from flask import Flask, render_template
from routes.auth import auth_bp
import os
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

csrf = CSRFProtect(app)

app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)