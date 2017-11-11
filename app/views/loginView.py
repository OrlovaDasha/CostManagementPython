import re

from flask import request, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user

from app import app, login_manager, db
from app.models.Users import Users


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        registered_user = Users.query.filter_by(username=username, password=password).first()

        try:
            if registered_user is None:
                username_confirmation = Users.query.filter_by(username = username).first()
                if username_confirmation is not None:
                    raise ValueError("Пароль для заданного пользователя неверный!")
                else:
                    raise ValueError("Такого пользователя не существует!")
        except Exception as e:
            return render_template("login.html", errors = e)


        remember = request.form.get("remember_me")
        login_user(registered_user, remember=remember)
        return redirect(url_for('index'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")
        email = request.form.get("email")

        email_rex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

        try:
            if username is None or not username:
                raise ValueError("Имя пользователя должно быть задано")
            if password is None or not password:
                raise ValueError("Пароль должен быть задан")
            if password != password_confirmation:
                raise ValueError("Пароли не совпадают")
            username_confirmation = Users.query.filter_by(username=username).first()
            if username_confirmation is not None:
                raise ValueError("Такое имя пользователя уже есть")

            regexp = re.compile(email_rex)

            if not regexp.match(email):
                raise ValueError("Email имеет неправильный вид")

        except Exception as e:
            return render_template("register.html", errors=e)

        try:
            user = Users(username, password, email)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template("register.html", errors=e)

        login_user(user, remember=True)
        return redirect(url_for("index"))