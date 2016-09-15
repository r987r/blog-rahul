from handler import Handler

class LogoutHandler(Handler):

    def get(self):
        self.redirect("/signup")
        self.response.headers.add_header(
            'Set-Cookie', str('username=; Path=/'))
