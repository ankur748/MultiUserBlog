from handlers import BlogHandler
from models import Post,Like,Comment

class OnePost(BlogHandler):
    def get(self, post_id):

        if self.is_cookie_valid():
            post    = Post.find_by_id(post_id)
            user_id = self.get_user_id()

            if not post:
                self.error(404)
            else:
                like    = Like.get_like(post_id, user_id)
                liked   = (like != None)

                is_owner = self.is_post_owner(post)
                comments = Comment.find_by_post(post_id)

                self.render('single_post.html',post=post,is_owner=is_owner,comments=comments,user_id=int(user_id),liked=liked,logged_in=True)
        else:
            self.redirect('/login')
