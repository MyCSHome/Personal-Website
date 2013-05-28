import webapp2
import logging
import json
import time
from main import jinja_environment
from google.appengine.ext import db
from google.appengine.api import memcache
 
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_environment.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
 
class BlogHandler(Handler):
    def get(self):
        blogs, time_point = get_blogs()
        
        if self.request.url.endswith('.json'):
            return self.render_json([p.as_dict() for p in blogs])
        else:
            dic = {"blogs" : blogs, "q_time" : time_point}
            html = jinja_environment.get_template('blog.html')
            self.response.out.write(html.render(dic))
            
    def render_json(self,d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)

last_query = time.time()    
def get_blogs(update = False):
    global last_query
    key = "top_ten"
    blogs = memcache.get(key)
    if blogs is None or update:
        last_query = time.time()
        blogs = db.GqlQuery("select * from Blog order by created desc limit 5")
        blogs = list(blogs)
        memcache.set(key, blogs)
    time_point = time.time() - last_query
    return blogs, int(time_point)



class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    
    def as_dict(self):
        d = {'subject' : self.subject,
             'content' : self.content,
             'created' : self.created.strftime('%c')}
        return d

