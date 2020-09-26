from flask import render_template,request,redirect,url_for,abort,flash
from . import main
# from ..request import get_quotes
from .forms import BlogForm,BioForm, CommentForm
from ..models import Blog,User, Comment
from flask_login import login_required,current_user
from .. import db,photos
from ..request import get_quote

@main.route('/')
@login_required
def index():
    quotes = get_quote()
    blogs = Blog.query.all()
    user_id = current_user.id
    user = User.query.filter_by(id=user_id).all()
    return render_template('index.html',blogs=blogs, user=user,quotes=quotes)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user.id
    blog = Blog.query.filter_by(user_id=user_id).all()

    if user is None:
        abort(404)
        
    return render_template("profile/profile.html", user=user, blog=blog)

@main.route('/new_blog', methods=['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        blog = form.blog.data
        title = form.title.data
        new_blog=Blog(blog=blog,title=title,user_id=current_user.id)
        
        new_blog.save_blog()
        
        return redirect(url_for('main.index'))
    
    return render_template('blogs.html', form=form)
        
@main.route('/new_comment/<int:blog_id>', methods=['GET','POST'])
@login_required
def new_comment(blog_id):
    form = CommentForm
    blogs = Blog.query.get(blog_id)
    comment = Comment.query.filter_by(blog_id=blog_id).all()
    form = CommentForm()
    if form.validate_on_submit():
        comments = form.comment.data
        title = form.title.data
        
        blog_id = blog_id
        user_id = current_user._get_current_object().id
        new_comment= Comment(comments=comments,title=title,blog_id=blog_id, user_id=user_id)
        new_comment.save_comment()      
       
        return redirect(url_for('main.index'))
    
    return render_template('comments.html', form=form, comment=comment, blog_id=blog_id)

@main.route('/user/<uname>/bio',methods = ['GET','POST'])
@login_required
def update_bio(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    bioform = BioForm()

    if bioform.validate_on_submit():
        user.bio = bioform.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/bio.html',bioform=bioform)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/blogs/<int:blog_id>/delete', methods = ['DELETE'])
@login_required
def delete(blog_id):
    blogs = Blog.query.get(blog_id)
    if blogs.user != current_user:
        abort(403)
    blogs.delete()
    flash("Blog succesfully deleted!")
    return redirect(url_for('main.index'))
        
        
    
    
        

