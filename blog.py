import users
from google.appengine.ext import db

class BlogEntry(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class MainHandler(users.Handler):	
	def render_front(self):
		entries = db.GqlQuery("select * from BlogEntry order by created desc")
		self.render("main.html", entries=entries)
	def get(self):
		self.render_front();
	
class NewPostHandler(users.Handler):	
	def render_front(self, subject="", content="", error=""):
		self.render("newpost.html", subject=subject, content=content, error=error)
	def get(self):
		self.render_front();
	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")
		
		if subject and content:
			a = BlogEntry(subject = subject, content = content)
			a.put()
			self.redirect("/" + str(a.key().id()))
		else:
			error = "We need both subject and artwork"
			self.render_front(subject, content, error);

class SinglePostHandler(users.Handler):
	def get(self, id):
		entries = BlogEntry.get_by_id(int(id))
		entries = [entries]
		self.render("main.html", entries=entries)
		
