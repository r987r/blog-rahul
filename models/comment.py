from blogPost import BlogPost
from google.appengine.ext import db


class Comment(db.Model):
    blogPost = db.ReferenceProperty(BlogPost, required=True)
    comment = db.TextProperty(required=True)
    username = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def comments_by_blogPost(cls, blogPost):
        return cls.all().filter('blogPost =', blogPost).order('-created')
    
    
    @classmethod
    def deleteComments_by_blogPost_id(cls, uid):
        return cls.deleteComments_by_blogPost(BlogPost.blogPost_by_id(uid))
    
    @classmethod
    def deleteComments_by_blogPost(cls, blogPost):
        comments = cls.comments_by_blogPost(blogPost)
        for comment in comments:
            comment.delete()

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
