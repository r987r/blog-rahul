import webapp2
import users
import blog

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=blog.MainHandler, name='main'),
    webapp2.Route(r'/signup', handler=users.SignUpHandler, name='signup'),
    webapp2.Route(r'/login', handler=users.LoginHandler, name='login'),
    webapp2.Route(r'/logout', handler=users.LogoutHandler, name='logout'),
    webapp2.Route(r'/welcome', handler=users.WelcomeHandler, name='welcomehandler'),
    webapp2.Route(r'/newpost', handler=blog.NewPostHandler, name='newpost'),
    webapp2.Route(r'/#\?.+', handler=blog.MainHandler, name='querymain'),

], debug=True)
