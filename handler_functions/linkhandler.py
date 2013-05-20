import webapp2
from newbloghandler import Blog
from newbloghandler import Handler
class LinkHandler(Handler):
    def get(self, id):
        blog = Blog.get_by_id(int(id))
        if blog:
            self.render("perlink.html", blog=blog)
        else:
            self.write("the blog doesn't exist")
