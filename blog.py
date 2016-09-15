import sys

from handler import Handler
from blogPost import BlogPost
from comment import Comment
import users
import datetime

from google.appengine.ext import db


class MainHandler(Handler):

    def get(self):
        blogPosts = BlogPost.blogPosts_all()
        self.render("main.html", blogPosts=blogPosts)


class UserHandler(Handler):

    def get(self, u):
        blogPosts = BlogPost.blogPosts_by_username(u)
        if blogPosts.get():
            self.render("userposts.html", blogPosts=blogPosts, username=u)
        else:
            self.redirect("/")


class OnePostHandler(Handler):

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


class PostHandler(Handler):

    def get(self):
        Handler.get(self)

    def render_front(self, subject="", content="", error=""):
        self.render(
            "posthandler.html",
            subject=subject,
            content=content,
            error=error)

    def valid_post(self):
        self.subject = self.request.get("subject")
        self.content = self.request.get("content")
        cancel = self.request.POST.get("cancel_item", None)
        if(cancel):
            self.redirect(self.getReferer())
            return False
        elif not (self.subject and self.content):
            error = "We need both subject and content"
            self.render_front(self.subject, self.content, error)
            return False
        return True


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


class DeletePostHandler(Handler):

    def get(self, uid):
        Handler.get(self)
        blogPost = BlogPost.blogPost_by_id(uid)
        if blogPost and blogPost.isMyPost(self.user.username):
            self.render("deletepost.html")
        else:
            self.render("errorhandler.html", error="Invalid Delete Detected")

    def post(self, uid):
        cancel = self.request.POST.get("cancel_item", None)
        if cancel:
            self.redirect(self.getReferer())
        else:
            BlogPost.deleteBlogPost(uid)
            self.redirect("/")


class CommentHandler(Handler):

    def get(self, uid):
        Handler.get(self)
        comment = Comment.comment_by_id(uid)
        if comment and comment.isMyComment(self.user.username):
            self.render("editcomment.html", sub_comment=comment.comment)
        else:
            self.render(
                "errorhandler.html",
                error="Invalid Comment Edit Detected")

    def post(self, uid):
        cancel = self.request.POST.get("cancel_item", None)
        delete = self.request.POST.get("delete_item", None)
        success = True
        if cancel:
            pass
        elif delete:
            Comment.deleteComment(uid)
        else:
            sub_comment = self.request.get("sub_comment")
            if sub_comment:
                comment = Comment.comment_by_id(uid)
                comment.comment = sub_comment
                comment.modified = datetime.datetime.now()
                comment.put()
            else:
                error = "We need a valid comment!"
                success = False
        if success:
            self.redirect(self.getReferer())
        else:
            self.render("editcomment.html", error=error)
