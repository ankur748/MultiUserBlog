from handlers import BlogHandler
from models import Post

#Blog Home Page
class HomePage(BlogHandler):
    def get(self):
        logged_in   = self.is_cookie_valid()
        posts       = Post.find_latest_posts()
        self.render('blog_home.html',posts=posts,logged_in=logged_in)
