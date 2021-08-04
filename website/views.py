from flask import Blueprint,  render_template, request
from flask.helpers import flash, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from werkzeug.utils import redirect
from .models import Posts, User
from . import db 

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    posts = Posts.query.order_by(Posts.date_created.desc())
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
            
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Posts.query.filter_by(id=id).first()

    if not post:
        flash('Post does not exist!', category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post!', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')
    return redirect(url_for('views.home'))

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(name=username).first()

    if not user:
        flash('Username does not exist', category='error')
        return redirect(url_for('views.home'))
    post = Posts.query.filter_by(author = user.id).all()
    return render_template("posts.html", user=current_user, posts = post, username = username)



