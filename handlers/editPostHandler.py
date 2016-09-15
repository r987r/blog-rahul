from postHandler import PostHandler
from blogPost import BlogPost
from comment import Comment
import datetime

class EditPostHandler(PostHandler):

    def get(self, uid):
        PostHandler.get(self)
        blogPost = BlogPost.blogPost_by_id(uid)
        if blogPost and blogPost.isMyPost(self.user.username):
            self.render_front(blogPost.subject, blogPost.content)
        else:
            self.render("errorhandler.html", error="Invalid Edit Detected")

    def post(self, uid):
        if self.valid_post():
            blogPost = BlogPost.blogPost_by_id(uid)
            blogPost.subject = self.subject
            blogPost.content = self.content
            blogPost.modified = datetime.datetime.now()
            blogPost.put()
            self.redirect("/uid/" + str(uid))

