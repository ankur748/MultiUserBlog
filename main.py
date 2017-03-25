import os
import webapp2
import jinja2
import re
import string
import hmac
import random
import time
from google.appengine.ext import db

#loading templates from templates directory and starting jinja environment with data escaped
template_dir    = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env       = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

#regexes used for valid inputs
USER_RE     = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE    = re.compile(r"^[\S]+@[\S]+.[\S]+$")

SECRET      = "EcstasyBlogSecret" #secret used for cookie hashing

#all global helper functions used

#salt generation used for password hashing
def generate_salt(length=5):
    return ''.join(random.choice(string.letters) for i in range(length))

#hash the given password with a salt used in sign up and password verification
def hash_password(password, salt=""):
    if not salt:
        salt = generate_salt()
    password_hash = str(hash_str(password, salt))
    return '%s|%s' % (password_hash,salt)

#used in both cookie and password hash generation
def hash_str(s, salt):
    return hmac.new(str(salt),str(s)).hexdigest()

#used for cookie generation
def make_secure_val(s, salt=SECRET):
    return '%s|%s' % (s,hash_str(s,salt))

#used for cookie verification
def check_secure_val(s, salt=SECRET):
    val = s.split('|')[0]
    if (s == make_secure_val(val,salt)):
        return val
    else:
        return None

#username regex matching
def valid_username(username):
    return USER_RE.match(username)

#password regex matching
def valid_password(password):
    return PASSWORD_RE.match(password)

#email regex matching
def valid_email(email):
    return EMAIL_RE.match(email)

def valid_password_hash(password_hash, password):

    salt = password_hash.split('|')[1]
    return password_hash == hash_password(password, salt)

#all model classes

#User model
class User(db.Model):
    username        = db.StringProperty(required = True)
    password_hash   = db.StringProperty(required = True)
    email           = db.StringProperty()
    created         = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def find_by_id(cls, userid):
        return User.get_by_id(userid)

    @classmethod
    def find_by_name(cls, name):
        return User.all().filter('username =', name.strip()).get()

    @classmethod
    def register_new_user(cls, username, password, email=None):
        password_hash = hash_password(password)
        return User(username=username,password_hash=password_hash,email=email)

    @classmethod
    def user_login(cls, username, password):
        user = cls.find_by_name(username)

        if user and valid_password_hash(user.password_hash, password):
            return user

#Blog model
class Post(db.Model):
    subject     = db.StringProperty(required = True)
    content     = db.TextProperty(required = True)
    user        = db.ReferenceProperty(User, collection_name = 'post_user', required = True)
    created     = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def find_latest_posts(cls, length=10):
        posts =  Post.all().order('-created').fetch(length)
        return posts

    @classmethod
    def find_by_user(cls, user_id):
        user = User.find_by_id(int(user_id))
        posts = Post.all().filter('user = ', user.key()).order('-created')
        return posts

    @classmethod
    def find_by_id(cls, postid):
        return Post.get_by_id(int(postid))

    @classmethod
    def save_new_post(cls, subject, content,user_id):
        user = User.find_by_id(int(user_id))
        return Post(subject=subject,content=content,user=user)

#Like model
class Like(db.Model):
    post    = db.ReferenceProperty(Post, collection_name = 'post', required = True)
    user    = db.ReferenceProperty(User, collection_name = 'like_user', required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def like_post(cls, post_id, user_id):
        post = Post.find_by_id(post_id)
        user = User.find_by_id(int(user_id))
        return Like(post=post, user=user)

    @classmethod
    def get_like(cls, post_id, user_id):
        post = Post.find_by_id(post_id)
        user = User.find_by_id(int(user_id))
        like = Like.all().filter('post = ', post.key()).filter('user = ', user.key()).get()

        return like

#Comment Model
class Comment(db.Model):
    post    = db.ReferenceProperty(Post, collection_name = 'comment_post', required = True)
    user    = db.ReferenceProperty(User, collection_name = 'comment_user', required = True)
    comment = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    edited  = db.DateTimeProperty(auto_now = True)

    @classmethod
    def comment_post(cls, post_id, user_id, comment):
        post = Post.find_by_id(post_id)
        user = User.find_by_id(int(user_id))
        return Comment(post=post, user=user, comment=comment)

    @classmethod
    def find_by_post(cls, post_id):
        post        = Post.find_by_id(int(post_id))
        return Comment.all().filter('post = ', post.key()).order('-edited').run()

    @classmethod
    def find_by_id(cls, comment_id):
        return Comment.get_by_id(int(comment_id))

#generic class used for creating common functions used
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#handling basic blog functions
class BlogHandler(Handler):

    def logout(self):
        userid = self.request.cookies.get("userid")
        if userid:
            self.response.headers.add_header('Set-Cookie', 'userid=; Path=/')

    def login(self, user):
        if user:
            user_id = user.key().id()
            self.response.headers.add_header('Set-Cookie', 'userid=%s; Path=/' % str(make_secure_val(user_id)))

    def is_cookie_valid(self):
        userid = self.request.cookies.get("userid")
        return userid and check_secure_val(userid)

    def get_user_id(self):
        userid = self.request.cookies.get("userid")
        if userid:
            return userid.split('|')[0]

    def is_post_owner(self,post):
        user_id         = self.get_user_id()
        if post:
            post_user_id    = str(post.user.key().id())
            return post_user_id == user_id
        else:
            return False

    def is_comment_owner(self,comment):
        user_id         = self.get_user_id()
        if comment:
            comment_user_id    = str(comment.user.key().id())
            return comment_user_id == user_id
        else:
            return False

#log out handler
class LogOut(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/login')

#log in handler
class LogIn(BlogHandler):

    def get(self):
        if self.is_cookie_valid():
            self.redirect('/')
        else:
            self.render('login.html')

    def post(self):

        username    = self.request.get("username")
        password    = self.request.get("password")

        user = User.user_login(username, password)

        if user:
            self.login(user)
            self.redirect('/')
        else:
            self.render('login.html',username=username,login_error=True)

#sign up handler
class SignUp(BlogHandler):

    def get(self):
        self.render('signup.html')

    def post(self):

        username    = self.request.get("username")
        password    = self.request.get("password")
        verify      = self.request.get("verify")
        email       = self.request.get("email")

        username_error = ""

        if not valid_username(username):
            username_error = "That's not a valid username."
        elif User.find_by_name(username):
            username_error = "The user already exists"

        password_error  = not(username_error) and (valid_password(password) == None)
        verify_error    = (not(username_error) and not(password_error) and ((password != "") and (password != verify)))
        email_error     = ((email != "") and (valid_email(email) == None))

        if (username_error or password_error or verify_error or email_error):
            self.render('signup.html', username=username,email=email,username_error=username_error,
                        password_error=password_error,verify_error=verify_error,email_error=email_error)
        else:
            user = User.register_new_user(username,password,email)
            user.put()
            self.login(user)
            self.redirect('/')

#Blog Home Page
class HomePage(BlogHandler):
    def get(self):
        logged_in   = self.is_cookie_valid()
        posts       = Post.find_latest_posts()
        self.render('blog_home.html',posts=posts,logged_in=logged_in)

#Find All My Posts
class MyPosts(BlogHandler):
    def get(self):
        if self.is_cookie_valid():
            logged_in   = True
            posts       = Post.find_by_user(self.get_user_id())
            self.render('my_posts.html',posts=posts,logged_in=logged_in)

# Single Post Handler
class OnePost(BlogHandler):
    def get(self, post_id):

        if self.is_cookie_valid():
            post    = Post.find_by_id(post_id)
            user_id = self.get_user_id()

            if not post:
                self.error(404)
            else:
                like    = Like.get_like(post_id, user_id)
                liked   = (like != None)

                is_owner = self.is_post_owner(post)
                comments = Comment.find_by_post(post_id)

                self.render('single_post.html',post=post,is_owner=is_owner,comments=comments,user_id=int(user_id),liked=liked,logged_in=True)
        else:
            self.redirect('/login')

#Create New Post
class NewPost(BlogHandler):

    def get(self):
        if self.is_cookie_valid():
            self.render("new_post.html",logged_in=True)
        else:
            self.redirect('/login')

    def post(self):

        if self.is_cookie_valid():
            subject   = self.request.get("subject")
            content   = self.request.get("content")

            if subject and content:
                post = Post.save_new_post(subject,content,self.get_user_id())
                post.put()
                self.redirect('/blogpost/%s' % str(post.key().id()))
            else:
                error = "Subject and Content, both please!!"
                self.render("new_post.html",subject=subject,content=content,error=error)
        else:
            self.redirect('/login')

#handles liking of post
class LikePost(BlogHandler):

    def get(self, post_id):

        if self.is_cookie_valid():
            post    = Post.find_by_id(post_id)
            userid  = self.get_user_id()

            if (not self.is_post_owner(post)):
                like = Like.like_post(post_id, userid)
                if like:
                    like.put()
                    time.sleep(0.1)
                    self.redirect('/blogpost/%s' % str(post_id))
                else:
                    self.error(404)
            else:
                self.redirect('/')
        else:
            self.redirect('/login')

#handles unliking of post
class UnlikePost(BlogHandler):

    def get(self, post_id):

        if self.is_cookie_valid():
            post    = Post.find_by_id(post_id)
            userid  = self.get_user_id()

            if (not self.is_post_owner(post)):
                like = Like.get_like(post_id, userid)
                if like:
                    like.delete()
                    time.sleep(0.1)
                    self.redirect('/blogpost/%s' % str(post_id))
                else:
                    self.error(404)
            else:
                self.redirect('/')
        else:
            self.redirect('/login')

#edit post handler
class EditPost(BlogHandler):

    def get(self, post_id):

        if self.is_cookie_valid():
            post    = Post.find_by_id(post_id)

            if (self.is_post_owner(post)):
                self.render('edit_post.html',post=post,logged_in=True)
            else:
                self.redirect('/')
        else:
            self.redirect('/login')

    def post(self, post_id):

        subject   = self.request.get("subject")
        content   = self.request.get("content")

        if self.is_cookie_valid():

            post    = Post.find_by_id(post_id)

            if (self.is_post_owner(post)):

                post.subject = subject
                post.content = content
                post.put()
                time.sleep(0.1)

                self.redirect('/blogpost/%s' % str(post.key().id()))
            else:
                self.redirect('/')
        else:
            self.redirect('/login')

#delete post handler
class DeletePost(BlogHandler):

    def get(self, post_id):

        if self.is_cookie_valid():
            post    = Post.find_by_id(post_id)

            if (self.is_post_owner(post)):
                self.render('delete_post.html',post=post,logged_in=True)
            else:
                self.redirect('/')
        else:
            self.redirect('/login')

    def post(self, post_id):

        if self.is_cookie_valid():
            post    = Post.find_by_id(post_id)

            if (self.is_post_owner(post)):
                post.delete()

            time.sleep(0.1)
            self.redirect('/')
        else:
            self.redirect('/login')

#post comment handler
class PostComment(BlogHandler):

    def post(self, post_id):

        if self.is_cookie_valid():
            comment     = self.request.get("comment")
            userid      = self.get_user_id()

            c = Comment.comment_post(post_id,userid,comment)
            c.put()
            time.sleep(0.1)

            self.redirect('/blogpost/%s' % str(post_id))
        else:
            self.redirect('/login')

#edit comment handler
class EditComment(BlogHandler):

    def get(self, comment_id):

        if self.is_cookie_valid():
            comment    = Comment.find_by_id(comment_id)

            if (self.is_comment_owner(comment)):
                self.render('edit_comment.html',comment=comment,logged_in=True)
            else:
                self.redirect('/')
        else:
            self.redirect('/login')

    def post(self, comment_id):

        comment_str   = self.request.get("comment")

        if self.is_cookie_valid():
            comment_obj    = Comment.find_by_id(comment_id)

            if (self.is_comment_owner(comment_obj)):

                comment_obj.comment = comment_str
                comment_obj.put()
                time.sleep(0.1)

                self.redirect('/blogpost/%s' % str(comment_obj.post.key().id()))
        else:
            self.redirect('/login')

#delete comment handler
class DeleteComment(BlogHandler):

    def get(self, comment_id):

        if self.is_cookie_valid():
            comment    = Comment.find_by_id(comment_id)

            if (self.is_comment_owner(comment)):
                self.render('delete_comment.html',comment=comment,logged_in=True)
            else:
                self.redirect('/')
        else:
            self.redirect('/login')

    def post(self, comment_id):

        if self.is_cookie_valid():
            comment    = Comment.find_by_id(comment_id)

            if (self.is_comment_owner(comment)):
                comment.delete()
                time.sleep(0.1)
                self.redirect('/blogpost/%s' % str(comment.post.key().id()))
            else:
                self.redirect('/')
        else:
            self.redirect('/login')

#redirection rules
app = webapp2.WSGIApplication([('/signup', SignUp),('/login', LogIn),('/myposts', MyPosts),
                                ('/logout', LogOut),('/', HomePage),('/newpost', NewPost),
                                ('/postcomment/([0-9]+)', PostComment), ('/editcomment/([0-9]+)', EditComment),
                                ('/editpost/([0-9]+)', EditPost), ('/deletepost/([0-9]+)', DeletePost),
                                ('/likepost/([0-9]+)', LikePost), ('/unlikepost/([0-9]+)', UnlikePost),
                                ('/blogpost/([0-9]+)', OnePost), ('/deletecomment/([0-9]+)', DeleteComment)], debug = True)
