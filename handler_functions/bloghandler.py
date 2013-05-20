import webapp2
import logging
from main import jinja_environment
from google.appengine.ext import db
from newbloghandler import Blog

class BlogHandler(webapp2.RequestHandler):
    def get(self):
        blogs = db.GqlQuery("select * from Blog order by created desc limit 5")
        dic = {"blogs" : blogs}
        html = jinja_environment.get_template('blog.html')
        self.response.out.write(html.render(dic))
    # def post(self):
        # text = self.request.get('text')
        # dic = {"value" : rot13(text)}
        # html = jinja_environment.get_template('rot.html')
        # self.response.out.write(html.render(dic))