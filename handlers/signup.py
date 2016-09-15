import re
from account import User
from handler import Handler

def valid_regex(regex, value):
    return re.compile(regex).match(value)


def chk_username(username):
    return valid_regex("^[a-zA-Z0-9_-]{3,20}$", username)


def chk_password(password):
    return valid_regex("^.{3,20}$", password)


def chk_email(email):
    return valid_regex("^[\S]+@[\S]+.[\S]+$", email)

class SignUpHandler(Handler):

    def get(self):
        self.render("signup.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        invalid_username = ""
        invalid_password = ""
        invalid_verify = ""
        invalid_email = ""

        if(not chk_username(username)):
            invalid_username = "That's not a valid username."
        if(not chk_password(password)):
            invalid_password = "That wasn't a valid password."
        if(password != verify):
            invalid_verify = "Your passwords didn't match."
        if(email and not chk_email(email)):
            invalid_email = "That's not a valid email."

        if(not (invalid_username or invalid_password or invalid_verify or invalid_email)):
            if(User.lookup_user(username)):
                invalid_username = "That user already exists."

        if(invalid_username or invalid_password or invalid_verify or invalid_email):
            self.render("signup.html", username=username, email=email,
                        invalid_username=invalid_username,
                        invalid_password=invalid_password,
                        invalid_verify=invalid_verify,
                        invalid_email=invalid_email)
        else:
            a = User.make_user(username, password, email)
            a.put()
            self.redirect("/welcome")
            self.response.headers.add_header(
                'Set-Cookie', str('username=%s|%s; Path=/' % (a.username, a.pw_hash)))
