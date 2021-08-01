from website import views
from flask import Blueprint, render_template, redirect, url_for,request, flash
from . import db
from .models import User 
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login",  methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        # cek apakah email user berada di dalam database
        user = User.query.filter_by(email = email).first()
        if user:
            # cek hash password cocok dengan yang berada di dalam database
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                # membuat session
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect!', category='error')
        else:
            flash('Email doest not exist!', category='error')


    return render_template("login.html")

@auth.route("/register" , methods=["POST", "GET"])
def register():
    # cek apakah request tersebut mengirim data user
    if request.method == 'POST':
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        
        # cek apakah email dan username telah di pakai
        email_exist = User.query.filter_by(email=email).first()
        name_exist = User.query.filter_by(name=name).first()
        if email_exist:
            flash('Email is already in use.', category='error')
        elif name_exist:
            flash('Username is already taken!', category='error')

        # cek panjang karakter username, password, dan email
        elif len(name) < 2 :
            flash('Username is too short', category='error')
        elif len(password) < 6:
            flash('Password must be 6 character or more!', category='error')
        elif len(email) < 4:
            flash('Email is invalid', category='error') 
        
        # jika pengecekan selesai user baru akan di tambahkan
        else:
            new_user = User(email = email, name = name, password = generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            # setelah user ditambahkan akan otomatis login
            login_user(new_user, remember=True)
            flash('User created!', category='success')
            return redirect(url_for('views.home'))
    
    return render_template("register.html")

@auth.route("/log-out")

# harus login sebelum mengeksekusi fungsi logout
@login_required
def logout():
    logout_user(current_user)
    return redirect(url_for(views.home))