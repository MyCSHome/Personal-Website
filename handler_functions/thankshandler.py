import webapp2
import re
from main import jinja_environment

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        username=self.request.get("username")
        USER = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        if not USER.match(username):
            self.redirect("/signup")
        else:
            self.response.out.write("welcome, %s!" %username)