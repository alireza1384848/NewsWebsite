from news import app, API_LOGIN_URL, API_NEWS_URL, API_SIGNUP_URL, forms, API_LOGOUT_URL, API_ADDNEWS_URL

from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash,abort
import requests
from datetime import timedelta,datetime

from news.forms import SignupForm, LoginForm, AddNewsForm,Confirmform


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    expire_date = datetime.utcnow() + timedelta(minutes=30)
    if request.cookies.get("access_token") is not None:
        rec = requests.post(API_LOGIN_URL, json={
            "access_token": request.cookies["access_token"]
        })
        if rec.status_code == 200:
            return redirect(url_for('index',username = rec.json()["username"]))
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        response = requests.post(API_LOGIN_URL, data={
            'username': username,
            'password': password,
            'exp_time' : 300 if remember else 30,
        })
        if remember:
            expire_date = datetime.utcnow() + timedelta(minutes=300)
        if response.status_code == 200:
            data = response.json()
            print(f'data is {data}')
            if data["role"] =="admin":
                    s = redirect(url_for('admin'))
                    s.set_cookie("access_token",data["access_token"],expires=expire_date)
                    return s
            else :
                    res =redirect(url_for('show_news',username = username))
                    expire_date = datetime.utcnow() + timedelta(minutes=30)
                    res.set_cookie('access_token', data['access_token'], expires=expire_date)
                    return res
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
        #confirm_password = form.confirm_password.data
                # ارسال داده‌ها به API برای ثبت‌نام
        if form.errors == {}:
            response = requests.post(API_SIGNUP_URL, json={
                        'username': username,
                        'email': email,
                        'password': password,
                        'rule' : "user"
            })
            if response.status_code == 200:
              return render_template("signup_success.html")
            elif response.status_code == 400:
                flash(f'نام کاربری تکراری است.', category='danger')
            else:
               return redirect(url_for('signup'))
    if form.errors != {}:
        print(form.errors)
        for err_msg in form.errors.values():
          flash(f'{str(err_msg)[2:-2]}', category='danger')

    return render_template('signup.html',form=form)

@app.route('/')
def show_news():
    username = request.args.get('username')
    if request.cookies.get('access_token') == None:
        return render_template("login_required_notice.html")

    else:
        #if request.cookies.get('access_token') is valid

         response = requests.get(
             API_NEWS_URL,
             headers={
                 "Authorization": f"Bearer { request.cookies['access_token']}"
             },
         )
         if response.status_code == 200:
             news_data = response.json()  # فرض می‌کنیم اخبار به این شکل برگشت می‌خوره
             print(news_data)
             RENDER = render_template('index.html', news=news_data, username=username,auth= True)
             return RENDER
         else:
             return redirect(url_for('signup'))


@app.route('/<int:id>')
def news_detail(id):
    response = requests.get(
        f'http://127.0.0.1:8000/news/{id}',
        headers={
            "Authorization": f"Bearer {request.cookies['access_token']}"
        },
    )
    if response.status_code == 200:
        news = response.json()
        print(news)
        return render_template('body_news.html', news=news)
    else:
        return 404

@app.route('/logout')
def logout():
    response = redirect(url_for('login'))
    response.set_cookie('access_token', '', expires=0)
    return response
@app.route('/admin')
def admin():
    try:
        response = requests.get(
            API_NEWS_URL,
            headers={
                "Authorization": f"Bearer {request.cookies['access_token']}"
            },
        )
        if response.status_code == 200:
            news_data = response.json()  # فرض می‌کنیم اخبار به این شکل برگشت می‌خوره
            return render_template('admin_page.html',news_list=news_data)
        else:
            abort(404)
    except Exception as e:
        abort(404)
@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    form  = AddNewsForm()
    image_url = form.image_url.data
    #date = form.date.data
    title = form.title.data
    summary =form.summary.data
    body = form.body.data
    if form.validate_on_submit():

        rec = requests.post(API_ADDNEWS_URL,json={
            'title': title,
            'body': body,
            'summary': summary ,
            'image_url': image_url,
            'date' : str(datetime.today().date()),
        },headers={
                "Authorization": f"{request.cookies['access_token']}"
            },)
        if rec.status_code == 200:
           return render_template("success.html")
    return render_template('admin_add_news.html',form = form)

@app.route('/delete_news/<int:id>', methods=['GET', 'POST'])
def delete_news(id):
            rec = requests.delete(f'http://127.0.0.1:8000/news/{id}' ,headers={
                "Authorization": f"{request.cookies['access_token']}"
            } )
            if rec.status_code == 200:
                flash('خبر با موفقیت حذف شد.', 'success')
                return redirect(url_for('admin'))
            else:
                abort(400)










