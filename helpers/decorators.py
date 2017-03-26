from functools import wraps
from models import *

def user_logged_in(function):
    @wraps(function)
    def wrapper (self, *args):
        if self.is_cookie_valid():
            return function(self, *args)
        else:
            self.redirect('/login')
    return wrapper

def post_exists(function):
    @wraps(function)
    def wrapper(self, *args):

        arglist = list(args)
        post_id = arglist[0]
        post    = Post.find_by_id(post_id)

        if post:
            arglist.append(post)
            return function(self, *arglist)
        else:
            self.error(404)
    return wrapper

def comment_exists(function):
    @wraps(function)
    def wrapper(self, *args):

        arglist     = list(args)
        comment_id  = arglist[0]
        comment     = Comment.find_by_id(comment_id)

        if comment:
            arglist.append(comment)
            return function(self, *arglist)
        else:
            self.error(404)
    return wrapper

def user_owns_post(function):
    @wraps(function)
    def wrapper (self, *args):

        arglist     = list(args)
        post        = arglist[1]

        if self.is_post_owner(post):
            return function(self, *args)
        else:
            self.redirect('/')

    return wrapper

def user_owns_comment(function):
    @wraps(function)
    def wrapper (self, *args):

        arglist     = list(args)
        comment     = arglist[1]

        if self.is_comment_owner(comment):
            return function(self, *args)
        else:
            self.redirect('/')
    return wrapper
