from handlers import BlogHandler
from models import Comment
import time
import helpers.decorators as decorators

user_logged_in      = decorators.user_logged_in
comment_exists      = decorators.comment_exists
user_owns_comment   = decorators.user_owns_comment

#delete comment handler
class DeleteComment(BlogHandler):

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def get(self, comment_id, comment):
        self.render('delete_comment.html',comment=comment,logged_in=True)

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def post(self, comment_id, comment):

        comment.delete()
        time.sleep(0.1)
        self.redirect('/blogpost/%s' % str(comment.post.key().id()))
