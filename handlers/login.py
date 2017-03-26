from handlers import BlogHandler
from models import User

class LogIn(BlogHandler):

    def get(self):
        if self.is_cookie_valid():
            self.redirect('/')
        else:
            self.render('login.html')

    def post(self):

        username    = self.request.get("username")
        password    = self.request.get("password")

        user        = User.find_by_name(username)

        if user and self.valid_password_hash(user.password_hash, password):
            self.login(user)
            self.redirect('/')
        else:
            self.render('login.html',username=username,login_error=True)
