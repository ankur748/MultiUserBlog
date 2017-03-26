from handlers import BlogHandler
from models import Post, Like
import time

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