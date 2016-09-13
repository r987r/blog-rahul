import users
import datetime
from google.appengine.ext import db

class BlogPost(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    username = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    modified = db.DateTimeProperty()
    comments = db.IntegerProperty(default = 0)
    likes = db.ListProperty(str)
    
    @classmethod
    def blogPosts_all(cls): 
        return cls.all().order('-created')

    @classmethod
    def blogPosts_by_username(cls, username): 
        return cls.all().filter('username =', username).order('-created')
    
    @classmethod
    def blogPost_by_id(cls, uid):
        return cls.get_by_id(int(uid))

    @classmethod
    def deleteBlogPost(cls, uid): 
        blogPost = cls.blogPost_by_id(uid)
        comments = blogPost.getComments();
        for comment in comments:
            comment.delete(); 
        blogPost.delete();
    
    def isMyPost(self, username):
        return username == self.username
  
    def hasLiked(self, username):
        return username in self.likes
    
    def likePost(self, username):
        if(self.hasLiked(username)):
            return False
        self.likes.append(username)
        self.put()
        return True
    
    def unLikePost(self, username):
        if(not self.hasLiked(username)):
            return False
        self.likes.remove(username)
        self.put()
        return True

    def getLikeString(self, username):
        if(not username or self.isMyPost(username)):
            return ""
        elif(self.hasLiked(username)):
            return '<a href="/uid/' + str(self.key().id()) + '/like">unlike</a>'
        else:
            return '<a href="/uid/' + str(self.key().id()) + '/like">like</a>'

    def getLikes(self):
        return len(self.likes)

    def addComment(self, comment):
        self.comments += 1
        self.put()
    
    def getComments(self):
        return Comment.comments_by_blogPost(self.key());

class Comment(db.Model):
    blogPost = db.ReferenceProperty(BlogPost, required = True)
    comment = db.TextProperty(required = True)
    username = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    modified = db.DateTimeProperty(auto_now = True)
    
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
    
class MainHandler(users.Handler):	
    def get(self):
        blogPosts = BlogPost.blogPosts_all()
        self.render("main.html", blogPosts=blogPosts)

class UserHandler(users.Handler):	
    def get(self, u):
        blogPosts = BlogPost.blogPosts_by_username(u)
        if blogPosts.get(): 
            self.render("userposts.html", blogPosts=blogPosts, username=u)
        else:
            self.redirect("/")

class OnePostHandler(users.Handler):	
    def get(self, uid):
        blogPost = BlogPost.blogPost_by_id(uid)
        if blogPost:
            comments = blogPost.getComments();
            self.render("onepost.html", blogPost=blogPost, comments=comments)
        else:
            self.redirect("/")

    def post(self, uid):
        comment = self.request.get("sub_comment")
        blogPost = BlogPost.blogPost_by_id(uid)
        blogKey = blogPost.key()
        if comment:
	    a = Comment(blogPost = blogKey, comment = comment, username = self.user.username)
	    a.put()
            blogPost.addComment(a)
	    self.redirect("/uid/" + str(uid))
        else:
	    error = "We need a valid comment!"
            self.render("onepost.html", blogPost=blogPost, error=error);

class LikeHandler(users.Handler):
    def get(self, uid):
            users.Handler.get(self)
            blogPost = BlogPost.blogPost_by_id(uid)
            if(not self.user or blogPost.isMyPost(self.user.username)):
                self.render("errorhandler.html", "Invalid Like detected");
            else:
                if(blogPost.hasLiked(self.user.username)):
                    blogPost.unLikePost(self.user.username)
                else:
                    blogPost.likePost(self.user.username)
                self.redirect(self.getReferer())

class PostHandler(users.Handler):	
    def get(self):
        users.Handler.get(self)
    def render_front(self, subject="", content="", error=""):
        self.render("posthandler.html", subject=subject, content=content, error=error)
    def valid_post(self):
        self.subject = self.request.get("subject")
        self.content = self.request.get("content")
        cancel = self.request.POST.get("cancel_item", None)	
        if(cancel):
            self.redirect(self.getReferer())
            return False
        elif not (self.subject and self.content):
    	    error = "We need both subject and content"
    	    self.render_front(self.subject, self.content, error);
            return False
        return True
            
class NewPostHandler(PostHandler):	
    def get(self):
        PostHandler.get(self)
        if(self.user):
	    self.render_front();
        else:
            self.redirect("/login")
    def post(self):
	if self.valid_post():
	    a = BlogPost(subject = self.subject, content = self.content, username = self.user.username)
	    a.put()
	    self.redirect("/uid/" + str(a.key().id()))
            
class EditPostHandler(PostHandler):	
    def get(self, uid):
        PostHandler.get(self)
        blogPost = BlogPost.blogPost_by_id(uid)
        if blogPost and blogPost.isMyPost(self.user.username):
            self.render_front(blogPost.subject, blogPost.content)
        else:
            self.render("errorhandler.html", error="Invalid Edit Detected");
	
    def post(self, uid):
	if self.valid_post():
              blogPost = BlogPost.blogPost_by_id(uid)
	      blogPost.subject = self.subject
              blogPost.content = self.content
              blogPost.modified = datetime.datetime.now()
              blogPost.put()
	      self.redirect("/uid/" + str(uid))

class DeletePostHandler(users.Handler):
    def get(self, uid):
        users.Handler.get(self)
        blogPost = BlogPost.blogPost_by_id(uid)
        if blogPost and blogPost.isMyPost(self.user.username):
            self.render("deletepost.html")
        else:
            self.render("errorhandler.html", error="Invalid Delete Detected");
    
    def post(self, uid):
        cancel = self.request.POST.get("cancel_item", None)	
        if cancel:
            self.redirect(self.getReferer())
        else:
            BlogPost.deleteBlogPost(uid)
            self.redirect("/")

class CommentHandler(users.Handler):
    def get(self, uid):
        users.Handler.get(self)
        comment = Comment.comment_by_id(uid)
        if comment and comment.isMyComment(self.user.username):
            self.render("editcomment.html", sub_comment = comment.comment)
        else:
            self.render("errorhandler.html", error="Invalid Comment Edit Detected");
    
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
            self.render("editcomment.html", error=error);

