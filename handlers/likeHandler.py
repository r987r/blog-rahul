from blogPost import BlogPost
from handler import Handler

class LikeHandler(Handler):

    def get(self, uid):
        Handler.get(self)
        blogPost = BlogPost.blogPost_by_id(uid)
        if(not self.user or blogPost.isMyPost(self.user.username)):
            self.render("errorhandler.html", "Invalid Like detected")
        else:
            if(blogPost.hasLiked(self.user.username)):
                blogPost.unLikePost(self.user.username)
            else:
                blogPost.likePost(self.user.username)
            self.redirect(self.getReferer())
