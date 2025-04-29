from datetime import timedelta
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.secret_key = 'ec9439cfc6c796ae2029594d'
bcrypt = Bcrypt(app)
app.permanent_session_lifetime = timedelta(minutes=15)  # برای logout خودکار


API_LOGIN_URL = 'http//127.0.0.1:8000/token'  # ← جایگزین کن
API_NEWS_URL = 'http//127.0.0.1:8000/news'
API_SIGNUP_URL = 'http//127.0.0.1:8000/signup'
API_LOGOUT_URL = 'http//127.0.0.1:8000/logout'
API_ADDNEWS_URL = 'http//127.0.0.1:8000/logout'
API_DELNEWS_URL = 'http//127.0.0.1:8000/logout'
from news import route

# admin : add_news _ delete_news