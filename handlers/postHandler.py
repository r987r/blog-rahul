from handler import Handler
from blogPost import BlogPost

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

