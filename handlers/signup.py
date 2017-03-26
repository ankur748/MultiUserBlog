import re
from handlers import BlogHandler
from models import User

#regexes used for valid inputs
USER_RE     = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE    = re.compile(r"^[\S]+@[\S]+.[\S]+$")

#username regex matching
def valid_username(username):
    return USER_RE.match(username)

#password regex matching
def valid_password(password):
    return PASSWORD_RE.match(password)

#email regex matching
def valid_email(email):
    return EMAIL_RE.match(email)

class SignUp(BlogHandler):

    def get(self):
        self.render('signup.html')

    def post(self):

        username    = self.request.get("username")
        password    = self.request.get("password")
        verify      = self.request.get("verify")
        email       = self.request.get("email")

        username_error = ""

        if not valid_username(username):
            username_error = "That's not a valid username."
        elif User.find_by_name(username):
            username_error = "The user already exists"

        password_error  = not(username_error) and (valid_password(password) == None)
        verify_error    = (not(username_error) and not(password_error) and ((password != "") and (password != verify)))
        email_error     = ((email != "") and (valid_email(email) == None))

        if (username_error or password_error or verify_error or email_error):
            self.render('signup.html', username=username,email=email,username_error=username_error,
                        password_error=password_error,verify_error=verify_error,email_error=email_error)
        else:
            password_hash   = self.hash_password(password)
            user            = User.register_new_user(username,password_hash,email)

            user.put()
            self.login(user)
            self.redirect('/')
