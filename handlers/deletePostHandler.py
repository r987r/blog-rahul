from handler import Handler
from blogPost import BlogPost
from comment import Comment

class DeletePostHandler(Handler):

    def valid_delete(self, uid):
        blogPost = BlogPost.blogPost_by_id(uid)
        if blogPost and blogPost.isMyPost(self.user.username):
            return blogPost
        return None

    def get(self, uid):
        Handler.get(self)
        blogPost = self.valid_delete(uid)
        if(blogPost):
            self.render("deletepost.html")
        else:
            self.render("errorhandler.html", error="Invalid Delete Detected")

    def post(self, uid):
        cancel = self.request.POST.get("cancel_item", None)
        blogPost = self.valid_delete(uid)
        if(not blogPost):
            self.render("errorhandler.html", error="Invalid Delete Detected")
        elif cancel:
            self.redirect(self.getReferer())
        else:
            Comment.deleteComments_by_blogPost_id(uid)
            BlogPost.deleteBlogPost(uid)
            self.redirect("/")
