import webapp2
from main import jinja_environment
from google.appengine.ext import db

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_environment.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class NewBlogHandler(Handler):
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
            id = b.key().id()
            self.redirect("/blog/%d" % id)
        else:
            error = "we need both subject and content"
            self.new_blog(subject, content, error)
       