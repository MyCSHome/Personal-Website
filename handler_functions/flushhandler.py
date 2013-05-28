import webapp2

from bloghandler import Handler

from google.appengine.api import memcache

class FlushHandler(Handler):
    def get(self):
        memcache.flush_all()
        self.redirect("/blog")

    
  