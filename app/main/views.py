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
