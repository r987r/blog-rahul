from blogPost import BlogPost
from google.appengine.ext import db


class Comment(db.Model):
    blogPost = db.ReferenceProperty(BlogPost, required=True)
    comment = db.TextProperty(required=True)
    username = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def comments_by_blogPost(cls, blogEntry):
        return cls.all().filter('blogPost =', blogEntry).order('-created')

    @classmethod
    def comment_by_id(cls, uid):
        return cls.get_by_id(int(uid))

    @classmethod
    def deleteComment(cls, uid):
        comment = cls.comment_by_id(uid)
        comment.blogPost.comments -= 1
        comment.delete()
        comment.blogPost.put()

    def isMyComment(self, username):
        return username == self.username
