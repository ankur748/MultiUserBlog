import webapp2
import time
from handlers import *

#redirection rules
app = webapp2.WSGIApplication([('/signup', SignUp),('/login', LogIn),('/myposts', MyPosts),
                                ('/logout', LogOut),('/', HomePage),('/newpost', NewPost),
                                ('/postcomment/([0-9]+)', PostComment), ('/editcomment/([0-9]+)', EditComment),
                                ('/editpost/([0-9]+)', EditPost), ('/deletepost/([0-9]+)', DeletePost),
                                ('/likepost/([0-9]+)', LikePost), ('/unlikepost/([0-9]+)', UnlikePost),
                                ('/blogpost/([0-9]+)', OnePost), ('/deletecomment/([0-9]+)', DeleteComment)], debug = True)
