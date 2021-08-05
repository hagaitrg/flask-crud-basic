from website import auth
from flask import Blueprint,  render_template, request
from flask.helpers import flash, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from werkzeug.utils import redirect
from .models import Comments, Posts, User
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

@views.route("/edit-post/<id>")
@login_required
def edit_post(id):
    post = Posts.query.filter_by(id=id).first()
    if not post:
        flash('Post does not exist!', category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to edit this post!', category='error')
    else:
        return render_template("edit_post.html", user=current_user, post = post)

@views.route("/update-post/<id>", methods=["POST", "GET"])
@login_required
def update_post(id):
    if request.method == "POST":
        p = Posts.query.filter_by(id=id).first()
        text = request.form.get('post')
        author = current_user.id

        if text:
            # fixed by jeddenkah 
            p.post = text
            p.author = author
            db.session.commit()
            flash('Post Edited!', category='success')
            return redirect(url_for("views.home"))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(name=username).first()

    if not user:
        flash('Username does not exist', category='error')
        return redirect(url_for('views.home'))
    post = user.posts
    return render_template("posts.html", user=current_user, posts = post, username = username)

@views.route("/create-comment/<post_id>", methods=["GET", "POST"])
@login_required
def create_commnet(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty!', category="error")
    else:
        post = Posts.query.filter_by(id = post_id)
        if post:
            comment = Comments(text=text, author = current_user.id, post_id = post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('post dsoes not exists!', category="error")

    return redirect(url_for('views.home'))

@views.route("/delete-comment/<id>")
@login_required
def delete_comment(id):
    comment = Comments.query.filter_by(id=id).first()

    if not comment:
        flash('Comment does not exist!', category='error')
    elif current_user.id != comment.author and current_user.id != comment.posts.author:
        flash('You do not have permission to delete this comment!', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted', category='success')
    return redirect(url_for('views.home'))