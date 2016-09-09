
import users
from google.appengine.ext import db

class BlogPost(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    username = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    comments = db.IntegerProperty(default = 0)
    likes = db.ListProperty(db.Key)
    
    @classmethod
    def blogPosts_all(cls): 
        return cls.all()

    @classmethod
    def blogPosts_by_username(cls, username): 
        return cls.all().filter('username =', username)
    
    @classmethod
    def blogPost_by_id(cls, uid):
        return cls.get_by_id(int(uid))
    #@classmethod
    #def changeLike(cls, blogPost):

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
    
    @classmethod
    def comments_by_blogPost(cls, blogEntry): 
        return cls.all().filter('blogPost =', blogEntry)
    

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
		if not self.user:
                        error = "You must sign in"
			self.render("onepost.html", blogPost=blogPost, error=error);
                elif comment:
			a = Comment(blogPost = blogKey, comment = comment, username = self.user.username)
			a.put()
                        blogPost.addComment(a)
			self.redirect("/uid/" + str(uid))
		else:
			error = "We need a valid comment!"
			self.render("onepost.html", blogPost=blogPost, error=error);
	
class NewPostHandler(users.Handler):	
	def render_front(self, subject="", content="", error=""):
		self.render("newpost.html", subject=subject, content=content, error=error)
	def get(self):
                if(self.user):
		    self.render_front();
                else:
                    self.redirect("/login")
	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")
		
		if subject and content:
			a = BlogPost(subject = subject, content = content, username = self.user.username)
			a.put()
			self.redirect("/uid/" + str(a.key().id()))
		else:
			error = "We need both subject and artwork"
			self.render_front(subject, content, error);

