import users
from google.appengine.ext import db

class BlogEntry(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    username = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    likes = db.ListProperty(db.Key)
    comments = db.ListProperty(db.Key)
    
    @classmethod
    def entries_all(cls): 
        return cls.all()

    @classmethod
    def entries_by_username(cls, username): 
        return cls.all().filter('username =', username)
    
    @classmethod
    def entry_by_id(cls, uid):
        return cls.get_by_id(int(uid))
    #@classmethod
    #def changeLike(cls, blogEntry):

    #@classmethod
    #def getLikes(cls, blogEntry):
    
    #@classmethod
    #def addComment(cls, comment):

    #@classmethod
    #def getComments(cls, blogEntry):
 

class Comment(db.Model):
    blogEntry = db.ReferenceProperty(BlogEntry, required = True)
    comment = db.TextProperty(required = True)
    user = db.ReferenceProperty(users.User, required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainHandler(users.Handler):	
	def get(self):
		u = self.request.get("u")
	        uid = self.request.get("uid")
                if(u):
                    entries = BlogEntry.entries_by_username(u) 
                elif(uid):
                    entries = [ BlogEntry.entry_by_id(uid) ]
                else:
                    entries = BlogEntry.entries_all()
                self.render("main.html", entries=entries)
	
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
			a = BlogEntry(subject = subject, content = content, username = self.user.username)
			a.put()
			self.redirect("/?uid=" + str(a.key().id()))
		else:
			error = "We need both subject and artwork"
			self.render_front(subject, content, error);

