import webapp2
import logging
import json
from main import jinja_environment
from google.appengine.ext import db
from newbloghandler import Blog
from newbloghandler import Handler

class BlogHandler(Handler):
    def get(self):
        blogs = db.GqlQuery("select * from Blog order by created desc limit 5")
        dic = {"blogs" : blogs}
        if self.request.url.endswith('.json'):
            return self.render_json([p.as_dict() for p in blogs])
        else:
            html = jinja_environment.get_template('blog.html')
            self.response.out.write(html.render(dic))
            
    def render_json(self,d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)


