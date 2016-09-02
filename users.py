import base
import webapp2
import re
import hashlib
import random
import string

from google.appengine.ext import db

hash_seed = "vumb;gtink2;rahul;twenty"

def valid_regex(regex, value):
    return re.compile(regex).match(value)	
def chk_username(username):
	return valid_regex("^[a-zA-Z0-9_-]{3,20}$", username);
def chk_password(password):
	return valid_regex("^.{3,20}$", password);
def chk_email(email):
	return valid_regex("^[\S]+@[\S]+.[\S]+$",email);
	
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw):
    salt = make_salt()
    h = hashlib.sha256(hash_seed + name + pw + salt).hexdigest()
    return h, salt

def valid_pw(name, pw, salt, check_hash):
    if(hashlib.sha256(hash_seed + name + pw + salt).hexdigest() == check_hash):
        return True
    else:
        return False

def lookup_user(username):
	return db.GqlQuery("select * from User where username = '%s'" % username).get()

def check_credentials(username, password):
	user = lookup_user(username)
	if(user and valid_pw(username, password, user.salt, user.pw_hash)):
		return user.pw_hash

def valid_username_cookie(username, pw_hash):
	#DB lookup here for user
	user = lookup_user(username)
	if(user and user.pw_hash == pw_hash):
		return True
	else:
		return False
	
class User(db.Model):
	username = db.StringProperty(required = True)
	pw_hash = db.StringProperty(required = True)
	salt = db.StringProperty(required = True)
	email = db.StringProperty(required = False)
	
class SignUpHandler(base.Handler):	
	def get(self):
		self.render("signup.html")
	
	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')
		invalid_username = "";
		invalid_password = "";
		invalid_verify = "";
		invalid_email = "";
		
		if(not chk_username(username)):
			invalid_username = "That's not a valid username.";
		if(not chk_password(password)):
			invalid_password = "That wasn't a valid password.";
		if(password != verify):
			invalid_verify = "Your passwords didn't match."
		if(email and not chk_email(email)):
			invalid_email = "That's not a valid email."

		if(not (invalid_username or invalid_password or invalid_verify or invalid_email)):
			if(lookup_user(username)):
				invalid_username = "That user already exists.";
				
		if(invalid_username or invalid_password or invalid_verify or invalid_email):
			self.render("signup.html", username=username, email=email,
							invalid_username=invalid_username,
							invalid_password=invalid_password,
							invalid_verify=invalid_verify,
							invalid_email=invalid_email)
		else:
			pw_hash, salt = make_pw_hash(username, password)
			a = User(username=username, pw_hash=pw_hash, email=email, salt=salt)
			a.put()
			self.redirect("/welcome"); 
			self.response.headers.add_header('Set-Cookie', str('username=%s|%s; Path=/' % (username,pw_hash)))
		
class LoginHandler(base.Handler):
	def get(self):
		self.render("login.html")

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		
		#inval cookie check needed here
		pw_hash = check_credentials(username,password)
		if(not pw_hash):
			self.render("login.html", login_error="Invalid login")
		else:
			self.redirect("/welcome")
			self.response.headers.add_header('Set-Cookie', str('username=%s|%s; Path=/' % (username,pw_hash)))

class LogoutHandler(base.Handler):
	def get(self):
		self.redirect("/signup")
		self.response.headers.add_header('Set-Cookie', str('username=; Path=/'))

			
class WelcomeHandler(base.Handler):	
	def get(self):
		username = self.request.cookies.get('username','0|0')
		username = username.split('|')
		
		#inval cookie check needed here
		if(len(username)==2 and valid_username_cookie(username[0], username[1])):
			self.render("thanks.html", username=username[0])
		else:
			self.redirect("/signup")
	
