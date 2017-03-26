from handlers import BlogHandler
from models import Comment
import time

#delete comment handler
class DeleteComment(BlogHandler):

    def get(self, comment_id):

        if self.is_cookie_valid():
            comment    = Comment.find_by_id(comment_id)

            if (self.is_comment_owner(comment)):
                self.render('delete_comment.html',comment=comment,logged_in=True)
            else:
                self.redirect('/')
        else:
            self.redirect('/login')

    def post(self, comment_id):

        if self.is_cookie_valid():
            comment    = Comment.find_by_id(comment_id)

            if (self.is_comment_owner(comment)):
                comment.delete()
                time.sleep(0.1)
                self.redirect('/blogpost/%s' % str(comment.post.key().id()))
            else:
                self.redirect('/')
        else:
            self.redirect('/login')
