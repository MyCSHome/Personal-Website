import webapp2
import json
from newbloghandler import Blog
from newbloghandler import Handler

class LinkHandler(Handler):
    def get(self, id):
        blog = Blog.get_by_id(int(id))
        if blog:
            if self.request.url.endswith('.json'):
                self.render_json(blog.as_dict())
            else:
                self.render("perlink.html", blog=blog)
        else:
            self.write("the blog doesn't exist")
    
    def post(self,id):
        blog = Blog.get_by_id(int(id))
        blog.delete()
        self.redirect("/blog")
   
    
    def render_json(self,d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)
