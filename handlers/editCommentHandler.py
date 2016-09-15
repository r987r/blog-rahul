from handler import Handler
from comment import Comment
import datetime

class EditCommentHandler(Handler):

    def get(self, uid):
        Handler.get(self)
        comment = Comment.comment_by_id(uid)
        if comment and comment.isMyComment(self.user.username):
            self.render("editcomment.html", sub_comment=comment.comment)
        else:
            self.render(
                "errorhandler.html",
                error="Invalid Comment Edit Detected")

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
            self.render("editcomment.html", error=error)
