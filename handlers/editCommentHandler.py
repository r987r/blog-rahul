from handler import Handler
from comment import Comment
import datetime

class EditCommentHandler(Handler):

    def valid_edit(self, uid):
        comment = Comment.comment_by_id(uid)
        if comment and comment.isMyComment(self.user.username):
            return comment
        return None 

    def get(self, uid):
        Handler.get(self)
        comment = self.valid_edit(uid)
        if(comment):
            self.render("editcomment.html", sub_comment=comment.comment)
        else:
            self.render(
                "errorhandler.html",
                error="Invalid Comment Edit Detected")

    def post(self, uid):
        cancel = self.request.POST.get("cancel_item", None)
        delete = self.request.POST.get("delete_item", None)
        comment = self.valid_edit(uid)
        if(not comment):
            self.render(
                "errorhandler.html",
                error="Invalid Comment Edit Detected")
        elif cancel:
            self.redirect(self.getReferer())
        elif delete:
            Comment.deleteComment(uid)
            self.redirect(self.getReferer())
        else:
            sub_comment = self.request.get("sub_comment")
            if sub_comment:
                comment = Comment.comment_by_id(uid)
                comment.comment = sub_comment
                comment.modified = datetime.datetime.now()
                comment.put()
                self.redirect(self.getReferer())
            else:
                error = "We need a valid comment!"
                success = False
                self.render("editcomment.html", error=error)
