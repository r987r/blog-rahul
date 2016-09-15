import os
import sys
sys.path.insert(0, sys.path[0] + '/models')
sys.path.insert(0, sys.path[1] + '/handlers')
import webapp2
import blog
from signup import SignUpHandler
from login import LoginHandler
from logout import LogoutHandler
from welcome import WelcomeHandler

app = webapp2.WSGIApplication([
    webapp2.Route(r'/u/<u:\w+>', handler=blog.UserHandler, name='usermain'),
    webapp2.Route(r'/comment/<uid:\d+>/edit', handler=blog.CommentHandler, name='commenthandler'),
    webapp2.Route(r'/uid/<uid:\d+>/edit', handler=blog.EditPostHandler, name='edithandler'),
    webapp2.Route(r'/uid/<uid:\d+>/delete', handler=blog.DeletePostHandler, name='deletehandler'),
    webapp2.Route(r'/uid/<uid:\d+>/like', handler=blog.LikeHandler, name='likehandler'),
    webapp2.Route(r'/uid/<uid:\d+>', handler=blog.OnePostHandler, name='singlepost'),
    webapp2.Route(r'/', handler=blog.MainHandler, name='main'),
    webapp2.Route(r'/signup', handler=SignUpHandler, name='signup'),
    webapp2.Route(r'/login', handler=LoginHandler, name='login'),
    webapp2.Route(r'/logout', handler=LogoutHandler, name='logout'),
    webapp2.Route(r'/welcome', handler=WelcomeHandler, name='welcomehandler'),
    webapp2.Route(r'/newpost', handler=blog.NewPostHandler, name='newpost'),
], debug=True)
