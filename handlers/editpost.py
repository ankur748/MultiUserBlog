from handlers import BlogHandler
from models import Post
import time

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
