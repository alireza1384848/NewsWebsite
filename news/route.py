from news import app,API_LOGIN_URL,API_NEWS_URL,API_SIGNUP_URL,forms,API_LOGOUT_URL

from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash
import requests
from datetime import timedelta

from news.forms import SignupForm, LoginForm, AddNewsForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.cookies["access_token"] is None:
        rec = requests.post(API_SIGNUP_URL, json={
            "access_token": request.cookies["access_token"]
        })
        if rec.status_code == 200:
            return redirect(url_for('index',username = rec.json()["username"]))
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
        if remember:
            session.permanent = True  # فعال‌سازی ماندگاری سشن
        if response.status_code == 200:
            data = response.json()
            res =redirect(url_for('index',username = username))
            res.set_cookie('access_token', data['access_token'],expires=timedelta(minutes=30))
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
       #todo:page login nakarde
        return "error"

    else:
         response = requests.post(API_SIGNUP_URL, json={
            "access_token":request.cookies["access_token"]})
         if response.status_code == 200:
             news_data = response.json()  # فرض می‌کنیم اخبار به این شکل برگشت می‌خوره
         else:
             news_data = []
         RENDER =  render_template('index.html', news=news_data)
         return RENDER


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
    response = make_response()
    response.delete_cookie('access_token')
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
        # todo: functionality
        pass
    return render_template('admin_add_news.html',form = form)










