from handlers import BlogHandler
from models import Post
import helpers.decorators as decorators

user_logged_in      = decorators.user_logged_in

class MyPosts(BlogHandler):

    @user_logged_in
    def get(self):
        posts       = Post.find_by_user(self.get_user_id())
        self.render('my_posts.html',posts=posts,logged_in=True)
