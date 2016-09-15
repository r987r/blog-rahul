from handler import Handler

class WelcomeHandler(Handler):

    def get(self):
        if(self.user):
            self.render("welcome.html", username=self.user.username)
        else:
            self.redirect("/signup")
