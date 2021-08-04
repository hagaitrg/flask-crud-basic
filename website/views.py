from flask import Blueprint,  render_template, request
from flask.helpers import flash, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import Posts
from . import db 

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    posts = Posts.query.all()
    # menggunakan templating jinja 
    return render_template("home.html", user = current_user, posts = posts)

@views.route("/create-post", methods=["POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('post')

        if text:
            post = Posts(post=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post Created!', category="success")
            return redirect(url_for("views.home"))
            

