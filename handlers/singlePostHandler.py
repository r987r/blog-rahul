from handler import Handler
from blogPost import BlogPost
from comment import Comment

class SinglePostHandler(Handler):

    def get(self, uid):
        blogPost = BlogPost.blogPost_by_id(uid)
        if blogPost:
            comments = Comment.comments_by_blogPost(blogPost)
            self.render("onepost.html", blogPost=blogPost, comments=comments)
        else:
            self.redirect("/")

    def post(self, uid):
        comment = self.request.get("sub_comment")
        blogPost = BlogPost.blogPost_by_id(uid)
        blogKey = blogPost.key()
        if comment:
            a = Comment(
                blogPost=blogKey,
                comment=comment,
                username=self.user.username)
            a.put()
            blogPost.addComment()
            self.redirect("/uid/" + str(uid))
        else:
            error = "We need a valid comment!"
            self.render("onepost.html", blogPost=blogPost, error=error)
