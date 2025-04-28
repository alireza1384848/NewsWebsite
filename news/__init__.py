from datetime import timedelta
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.secret_key = 'ec9439cfc6c796ae2029594d'
bcrypt = Bcrypt(app)
app.permanent_session_lifetime = timedelta(minutes=15)  # برای logout خودکار


API_LOGIN_URL = 'http://your-api-url.com/api/login'  # ← جایگزین کن
API_NEWS_URL = 'http://your-api-url.com/api/news'
API_SIGNUP_URL = ''

from news import route

# admin : add_news _ delete_news