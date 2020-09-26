from flask import render_template,request,redirect,url_for,abort
from . import main
# from ..request import get_quotes
from .forms import BlogForm,BioForm, CommentForm
from ..models import Blog,User, Comment
from flask_login import login_required,current_user
from .. import db,photos

@main.route('/')
@login_required
def index():
    return render_template('index.html')

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user.id
    blog = Blog.query.filter_by(user_id=user_id).all()

    if user is None:
        abort(404)
        
    return render_template("profile/profile.html", user = user, blog=blog)
