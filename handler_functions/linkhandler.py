import webapp2
import json
import time
import logging
from bloghandler import Blog
from bloghandler import Handler
from bloghandler import get_blogs
import newbloghandler
from google.appengine.api import memcache


class LinkHandler(Handler):
    def get(self, id):
        blog = memcache.get(id)
        if int(id) in [20002,10002,9001,5001,1]:
            blog = Blog.get_by_id(int(id))
        if blog:
            if self.request.url.endswith('.json'):
                self.render_json(blog.as_dict())
            else:
                #logging.info(last_query)
                #logging.info(time.time())
                last_query = newbloghandler.last_query
                time_point =  time.time()- last_query
                #dic = {"blog" : blog, "q_time" : int(time_point)}
                self.render("perlink.html", blog=blog,q_time =int(time_point) )
        else:
            self.write("the blog doesn't exist")
    
    def post(self,id):
        blog = Blog.get_by_id(int(id))
        blog.delete()
        memcache.delete(id)
        get_blogs(True)
        self.redirect("/blog")
   
    
    def render_json(self,d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)
