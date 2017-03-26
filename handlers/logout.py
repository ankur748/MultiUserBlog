from handlers import BlogHandler

class LogOut(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/login')
