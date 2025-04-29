from news import app,API_LOGIN_URL,API_NEWS_URL,API_SIGNUP_URL,forms

from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash
import requests
from datetime import timedelta

from news.forms import SignupForm, LoginForm, AddNewsForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        if username == 'admin' and password == 'admin':
            return redirect(url_for('admin'))

        response = requests.post(API_LOGIN_URL, json={
            'username': username,
            'password': password
        })

        if response.status_code == 200:
            data = response.json()
            session['username'] = username
            session['role'] = data.get('role', 'user')  # فرض: API نقش کاربر رو برمی‌گردونه

            if remember:
                session.permanent = True  # فعال‌سازی ماندگاری سشن
            return redirect(url_for('home'))
        else:
            flash('نام کاربری یا رمز اشتباه است', 'danger')

    return render_template('login.html',form=form)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():

        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
                # ارسال داده‌ها به API برای ثبت‌نام
        if form.errors == {}:
            response = requests.post(API_SIGNUP_URL, json={
                        'username': username,
                        'email': email,
                        'password': password
            })
            if response.status_code == 201:
              return redirect(url_for('login'))
            else:
               return redirect(url_for('signup'))
    if form.errors != {}:
        print(form.errors)
        for err_msg in form.errors.values():
          flash(f'{str(err_msg)[2:-2]}', category='danger')

    return render_template('signup.html',form=form)
news_data =[]
@app.route('/')
def home():
    if request.cookies.get('username'):
        print(request.cookies)
        global news_data
    # response = requests.get(API_NEWS_URL)
    #
    # if response.status_code == 200:
    #     news_data = response.json()  # فرض می‌کنیم اخبار به این شکل برگشت می‌خوره
    # else:
    #     news_data = []
    # return render_template('index.html', news=news_data)
        news_data = [
        {
            "id": 1,
            "title": "خبر شماره 1",
            "summary": "خلاصه‌ای از خبر شماره 1...",
            "image_url": "https://via.placeholder.com/150",
            "body": "به نام خدا علیرضا روح الهی هستم 32 کا بانتی زدم !!"
        },
        {
            "id": 2,
            "title": "خبر شماره 2",
            "summary": "خلاصه‌ای از خبر شماره 2...",
            "image_url": "https://via.placeholder.com/150",
            "body": "به نام خدا علیرضا روح الهی هستم 32 کا بانتی زدم !!"
        }
    ]
        return render_template('index.html', news=news_data)

    else:
        print(request.cookies)
        response = make_response("cookie set!!")
        response.set_cookie("username", "admin",10)
        response.set_cookie("TOKEN", "jkdukahdklhkadhihasjlih",10)
        return response


def get_news_by_id(id):
     for tem in news_data:
         if tem['id'] == id:
             return tem


@app.route('/<int:id>')
def news_detail(id):
    news = get_news_by_id(id)  # اینو از API یا دیتابیس بیار
    return render_template('body_news.html', news=news)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/admin')
def admin():
    return render_template('admin_page.html',news_list=news_data)
@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    form  = AddNewsForm()
    author =form.author.data
    image_url = form.image_url.data
    date = form.date.data
    title = form.title.data
    summary =form.summary.data
    body = form.body.data
    if form.validate_on_submit():

        pass
    return render_template('admin_add_news.html',form = form)