from handlers import BlogHandler
from models import Post, Like
import time
import helpers.decorators as decorators

user_logged_in      = decorators.user_logged_in
post_exists         = decorators.post_exists

class UnlikePost(BlogHandler):

    @user_logged_in
    @post_exists
    def get(self, post_id, post):

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
