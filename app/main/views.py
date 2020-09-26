from flask import render_template,request,redirect,url_for,abort
from . import main
from ..request import get_quotes
from .forms import BlogForm,Bioform, CommentForm
from ..models import Blog,User, Comments
from flask_login import login_required,current_user
from .. import db,photos
import markdown2