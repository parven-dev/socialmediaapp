import os.path
import random
from functools import wraps

from werkzeug.utils import secure_filename, redirect

from Main import app, db
from flask import render_template, request, flash, url_for, session
from Form import Form_Flask, Create_post, CommentForm, OTPForm
from database import Users, Post, CommentDatabase
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import bleach
from datetime import datetime
import uuid as uuid

from Smtp import MailServer

current_datetime = datetime.now()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(int(user_id))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("/index.html", post=posts)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect("home")

    form = Form_Flask(request.form)
    if request.method == "POST" or form.validate():
        username = form.user_name.data
        password = form.password.data
        user = Users.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("/login.html", login=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = Form_Flask(request.form)
    if request.method == "POST" or form.validate():
        username = form.user_name.data
        email = form.email.data
        already_user_in_database = Users.query.filter((Users.username == username) | (Users.email == email)).first()
        if already_user_in_database:
            if already_user_in_database.username == username:
                flash("Username already exist")
            if already_user_in_database.email == email:
                flash("Email Already Exists")
        else:
            otp = "".join([str(random.randint(0, 9)) for _ in range(6)])
            session['otp'] = otp
            session["form"] = {
                "username": form.user_name.data,
                "email": form.email.data,
                "password": form.password.data,
                "fullname": form.full_name.data
            }
            return redirect(url_for('otp_verification'))
    return render_template("/register.html", register=form)


def otp_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("otp"):
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper


@app.route("/otp_verification", methods=["GET", "POST"])
@otp_required
def otp_verification():
    form = OTPForm()
    form_data = session.get("form")
    expected_otp = session.get("otp")
    mail = MailServer(expected_otp, form_data["email"])
    mail.smtp_server()

    if request.method == "POST":
        enter_otp = request.form.get("otp")
        if enter_otp == expected_otp:
            username = form_data["username"]
            email = form_data["email"]
            password = form_data["password"]
            fullname = form_data["fullname"]

            register_to_database = Users(
                username=username,
                email=email,
                fullname=fullname,
            )
            register_to_database.set_password(password)
            db.session.add(register_to_database)
            db.session.commit()

            return redirect(url_for("login"))
    return render_template("/otp_verification.html", form=form)


@app.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    post_form = Create_post(request.form)
    if request.method == "POST" and post_form.validate():
        title = post_form.title.data
        subtitle = post_form.subtitle.data
        author = post_form.author.data
        content = post_form.content.data
        # senitized_content = bleach.clean(content, tags=[], strip=True)
        post = Post(
            title=title,
            subtitle=subtitle,
            author=author,
            content=content,
            user_id=current_user.id,
            time=datetime.now()
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("/create_post.html", post=post_form)


@app.route("/profile")
@login_required
def profile():
    return render_template("/profile.html")


@app.route("/edit_profile/<int:sno>/", methods=["GET", "POST"])
@login_required
def edit_profile(sno):
    user = Users.query.get_or_404(sno)
    form = Form_Flask(request.form)
    if request.method == "POST" or form.validate():
        user_name = form.user_name.data
        email_id = form.email.data
        fullname = form.full_name.data
        profile_picture = request.files.get("profile_picture")

        pic_filename = secure_filename(profile_picture.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], pic_name)
        profile_picture.save(filepath)

        if profile_picture:
            user.profile_picture = pic_name

        if user_name:
            user.username = user_name

        if email_id:
            user.email = email_id

        if fullname:
            user.fullname = fullname

        db.session.commit()
        return redirect(url_for("profile", sno=sno))

    return render_template("/edit_profile.html", register=form)


@app.route("/show_posts/<int:sno>", methods=["GET", "POST"])
def show_posts(sno):
    post = Post.query.get_or_404(sno)
    comments_form = CommentForm(request.form)
    if request.method == "POST" and comments_form.validate():
        comment = comments_form.comment.data
        comments = CommentDatabase(
            comment=comment,
            user_id=current_user.id,
            post_id=post.id,
            today=datetime.now()
        )
        db.session.add(comments)
        db.session.commit()
        return redirect(url_for("show_posts", sno=post.id))

    comment_data = CommentDatabase.query.filter_by(post_id=post.id).all()
    return render_template("show_posts.html", post=post,
                           form=comments_form, comment=comment_data)
