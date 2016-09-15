import os
import jinja2
import webapp2
from account import User
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        if(self.user):
            kw["user_in"] = self.user.username
        self.write(self.render_str(template, **kw))

    @staticmethod
    def valid_username_cookie(username):
        # DB lookup here for user
        username = username.split('|')
        if(not len(username) == 2):
            return None
        user = User.lookup_user(username[0])
        if(user and user.pw_hash == username[1]):
            return user
        else:
            return None

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        username = self.request.cookies.get('username', '0|0')
        self.user = Handler.valid_username_cookie(username)

    def get(self):
        self.response.headers.add_header(
            'Set-Cookie', str('referer=%s; Path=/' % self.request.referer))

    def getReferer(self):
        return str(self.request.cookies.get('referer', '/'))
