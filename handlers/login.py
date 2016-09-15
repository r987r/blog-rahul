from account import User
from handler import Handler

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
