from handler import Handler
from blogPost import BlogPost

class UserPostHandler(Handler):

    def get(self, u):
        blogPosts = BlogPost.blogPosts_by_username(u)
        if blogPosts.get():
            self.render("userposts.html", blogPosts=blogPosts, username=u)
        else:
            self.redirect("/")

