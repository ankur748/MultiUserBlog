from handlers import BlogHandler
from models import Post

class NewPost(BlogHandler):

    def get(self):
        if self.is_cookie_valid():
            self.render("new_post.html",logged_in=True)
        else:
            self.redirect('/login')

    def post(self):

        if self.is_cookie_valid():
            subject   = self.request.get("subject")
            content   = self.request.get("content")

            if subject and content:
                post = Post.save_new_post(subject,content,self.get_user_id())
                post.put()
                self.redirect('/blogpost/%s' % str(post.key().id()))
            else:
                error = "Subject and Content, both please!!"
                self.render("new_post.html",subject=subject,content=content,error=error)
        else:
            self.redirect('/login')
