from google.appengine.ext import db

class BlogPost(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    username = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty()
    comments = db.IntegerProperty(default=0)
    likes = db.ListProperty(str)

    @classmethod
    def blogPosts_all(cls):
        return cls.all().order('-created')

    @classmethod
    def deleteBlogPost(cls, uid):
        blogPost = cls.blogPost_by_id(uid)
        blogPost.delete()

    @classmethod
    def blogPosts_by_username(cls, username):
        return cls.all().filter('username =', username).order('-created')

    @classmethod
    def blogPost_by_id(cls, uid):
        return cls.get_by_id(int(uid))


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
            return '<a href="/uid/' + \
                str(self.key().id()) + '/like">unlike</a>'
        else:
            return '<a href="/uid/' + str(self.key().id()) + '/like">like</a>'

    def getLikes(self):
        return len(self.likes)

    def addComment(self):
        self.comments += 1
        self.put()
