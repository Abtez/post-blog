from . import db
from werkzeug.security import generate_password_hash,check_password_hash 
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255),index=True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    blogs = db.relationship('Blog',backref = 'blogger',lazy = "dynamic")
    comments = db.relationship('Comment',backref = 'feedback',lazy = "dynamic")
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
    
    def __repr__(self):
        return f'User {self.username}'
    
class Blog(db.Model):
    __tablename__ = 'blogs'
    
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    blog = db.Column(db.String(255),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    posted = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow())
    
    def save_blog(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_blog(cls,id):
        blogs = Blog.query.filter_by(user_id=id).all()
        return blogs

    
class Comment(db.Model):
    __tablename__ = 'comments' 
    
    id = db.Column(db.Integer, primary_key = True)
    comments = db.Column(db.Text(),nullable=False)
    title = db.Column(db.String(),nullable=False)
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_comments(cls,blog_id):
        comments = Comment.query.filter_by(blog_id=blog_id).all()

        return comments
        
    def __repr__(self):
        return f'Comment{self.comments}'
    
class Quote:
    def __init__(self,id, author, quote, link):
        self.id = id
        self.author = author
        self.quote = quote
        self.link = link
    