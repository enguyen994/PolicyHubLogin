from flask import Blueprint, request, render_template, redirect, session
from werkzeug.security import check_password_hash
from models.user import create_user, get_user_by_username
from config.ms_sso import get_microsoft_auth_url, exchange_code_for_token
import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            create_user(username, hashed_pw)
            return redirect('/')
    return render_template('signup.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = get_user_by_username(username)
    if user and check_password_hash(user['password'], password):
        session['user'] = username
        return redirect('/dashboard')
    return 'Invalid credentials', 401

@auth_bp.route('/microsoft')
def microsoft_login():
    return redirect(get_microsoft_auth_url())

@auth_bp.route('/microsoft/callback')
def microsoft_callback():
    code = request.args.get('code')
    token_info = exchange_code_for_token(code)
    if token_info:
        session['user'] = token_info.get('id_token')
        return redirect('/dashboard')
    return 'Microsoft login failed', 401