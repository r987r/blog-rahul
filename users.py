import jinja2
import webapp2
import re
from handler import Handler
from account import User
from google.appengine.ext import db


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


class LoginHandler(Handler):

    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        pw_hash = User.check_credentials(username, password)
        if(not pw_hash):
            self.render("login.html", login_error="Invalid login")
        else:
            self.redirect("/welcome")
            self.response.headers.add_header(
                'Set-Cookie', str('username=%s|%s; Path=/' % (username, pw_hash)))


class LogoutHandler(Handler):

    def get(self):
        self.redirect("/signup")
        self.response.headers.add_header(
            'Set-Cookie', str('username=; Path=/'))


class WelcomeHandler(Handler):

    def get(self):
        if(self.user):
            self.render("welcome.html", username=self.user.username)
        else:
            self.redirect("/signup")
