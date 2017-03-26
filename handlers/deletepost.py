from handlers import BlogHandler
from models import Post
import time

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
