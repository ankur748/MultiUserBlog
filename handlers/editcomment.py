from handlers import BlogHandler
from models import Comment
import time

class EditComment(BlogHandler):

    def get(self, comment_id):

        if self.is_cookie_valid():
            comment    = Comment.find_by_id(comment_id)

            if (self.is_comment_owner(comment)):
                self.render('edit_comment.html',comment=comment,logged_in=True)
            else:
                self.redirect('/')
        else:
            self.redirect('/login')

    def post(self, comment_id):

        comment_str   = self.request.get("comment")

        if self.is_cookie_valid():
            comment_obj    = Comment.find_by_id(comment_id)

            if (self.is_comment_owner(comment_obj)):

                comment_obj.comment = comment_str
                comment_obj.put()
                time.sleep(0.1)

                self.redirect('/blogpost/%s' % str(comment_obj.post.key().id()))
        else:
            self.redirect('/login')
