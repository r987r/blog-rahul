from postHandler import PostHandler
from blogPost import BlogPost

class NewPostHandler(PostHandler):

    def get(self):
        PostHandler.get(self)
        if(self.user):
            self.render_front()
        else:
            self.redirect("/login")

    def post(self):
        if self.valid_post():
            a = BlogPost(
                subject=self.subject,
                content=self.content,
                username=self.user.username)
            a.put()
            self.redirect("/uid/" + str(a.key().id()))


