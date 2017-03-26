from handlers import BlogHandler
from models import Comment
import time
import helpers.decorators as decorators

user_logged_in      = decorators.user_logged_in
comment_exists      = decorators.comment_exists
user_owns_comment   = decorators.user_owns_comment

class EditComment(BlogHandler):

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def get(self, comment_id, comment):

        self.render('edit_comment.html',comment=comment,logged_in=True)

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def post(self, comment_id, comment_obj):

        comment_str         = self.request.get("comment")
        comment_obj.comment = comment_str
        
        comment_obj.put()
        time.sleep(0.1)

        self.redirect('/blogpost/%s' % str(comment_obj.post.key().id()))
