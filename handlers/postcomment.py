from handlers import BlogHandler
from models import Comment
import time
import helpers.decorators as decorators

user_logged_in      = decorators.user_logged_in

class PostComment(BlogHandler):

    @user_logged_in
    def post(self, post_id):

        comment     = self.request.get("comment")
        userid      = self.get_user_id()

        c = Comment.comment_post(post_id,userid,comment)
        c.put()
        time.sleep(0.1)

        self.redirect('/blogpost/%s' % str(post_id))
