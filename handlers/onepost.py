from handlers import BlogHandler
from models import Post,Like,Comment
import helpers.decorators as decorators

user_logged_in  = decorators.user_logged_in
post_exists     = decorators.post_exists

class OnePost(BlogHandler):

    @post_exists
    @user_logged_in
    def get(self, post_id, post):

        user_id = self.get_user_id()

        like    = Like.get_like(post_id, user_id)
        liked   = (like != None)

        is_owner = self.is_post_owner(post)
        comments = Comment.find_by_post(post_id)

        self.render('single_post.html',post=post,is_owner=is_owner,comments=comments,user_id=int(user_id),liked=liked,logged_in=True)
