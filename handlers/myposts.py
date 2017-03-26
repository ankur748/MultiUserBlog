from handlers import BlogHandler
from models import Post

class MyPosts(BlogHandler):
    def get(self):
        if self.is_cookie_valid():
            logged_in   = True
            posts       = Post.find_by_user(self.get_user_id())
            self.render('my_posts.html',posts=posts,logged_in=logged_in)
