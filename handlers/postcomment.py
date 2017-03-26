from handlers import BlogHandler
from models import Comment
import time

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
