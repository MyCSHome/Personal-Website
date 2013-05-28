import webapp2
from main import jinja_environment
from google.appengine.ext import db
from bloghandler import get_blogs
from bloghandler import Blog
from bloghandler import Handler
from google.appengine.api import memcache
import time
last_query = time.time()
class NewBlogHandler(Handler):
    global last_query
    def new_blog(self, subject="", content="", error=""):
        self.render("newblog.html", subject=subject, content=content, error=error)
    
    def get(self):
        self.new_blog()
        
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        if subject and content:
            b = Blog(subject = subject, content = content)
            b.put()
            get_blogs(True)
            id = b.key().id()
            memcache.set(str(id), b)
            last_query = time.time()
            self.redirect("/blog/%d" % id)
        else:
            error = "we need both subject and content"
            self.new_blog(subject, content, error)
       