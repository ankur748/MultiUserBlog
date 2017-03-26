from handlers import BlogHandler
from models import Post
import helpers.decorators as decorators

user_logged_in = decorators.user_logged_in

class NewPost(BlogHandler):

    @user_logged_in
    def get(self):
        self.render("new_post.html",logged_in=True)

    @user_logged_in
    def post(self):

        subject   = self.request.get("subject")
        content   = self.request.get("content")

        if subject and content:
            post = Post.save_new_post(subject,content,self.get_user_id())
            post.put()
            self.redirect('/blogpost/%s' % str(post.key().id()))
        else:
            error = "Subject and Content, both please!!"
            self.render("new_post.html",subject=subject,content=content,error=error)
