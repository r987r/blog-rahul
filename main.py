import webapp2
import os
import sys
sys.path.insert(0, sys.path[0] + '/models')
sys.path.insert(0, sys.path[1] + '/handlers')

from handler import Handler
from blogPost import BlogPost
from signup import SignUpHandler
from login import LoginHandler
from logout import LogoutHandler
from welcome import WelcomeHandler
from userPostHandler import UserPostHandler
from singlePostHandler import SinglePostHandler
from likeHandler import LikeHandler
from newPostHandler import NewPostHandler
from editPostHandler import EditPostHandler
from deletePostHandler import DeletePostHandler
from editCommentHandler import EditCommentHandler

class MainHandler(Handler):

    def get(self):
        blogPosts = BlogPost.blogPosts_all()
        self.render("main.html", blogPosts=blogPosts)

app = webapp2.WSGIApplication([
    webapp2.Route(r'/u/<u:\w+>', handler=UserPostHandler, name='userpost'),
    webapp2.Route(r'/comment/<uid:\d+>/edit', handler=EditCommentHandler, name='comment'),
    webapp2.Route(r'/uid/<uid:\d+>/edit', handler=EditPostHandler, name='editpost'),
    webapp2.Route(r'/uid/<uid:\d+>/delete', handler=DeletePostHandler, name='deletepost'),
    webapp2.Route(r'/uid/<uid:\d+>/like', handler=LikeHandler, name='like'),
    webapp2.Route(r'/uid/<uid:\d+>', handler=SinglePostHandler, name='singlepost'),
    webapp2.Route(r'/', handler=MainHandler, name='main'),
    webapp2.Route(r'/signup', handler=SignUpHandler, name='signup'),
    webapp2.Route(r'/login', handler=LoginHandler, name='login'),
    webapp2.Route(r'/logout', handler=LogoutHandler, name='logout'),
    webapp2.Route(r'/welcome', handler=WelcomeHandler, name='welcome'),
    webapp2.Route(r'/newpost', handler=NewPostHandler, name='newpost'),
], debug=True)
