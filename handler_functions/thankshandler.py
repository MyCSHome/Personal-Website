import webapp2
import re
from main import jinja_environment
from signuphandler import User
import hashlib
import random
import string
class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        userr = self.request.cookies.get('user_id')
        if userr:
            id = userr.split('|')[0]
            user = User.get_by_id(int(id))
            if user:
                if user.encryption.split('|')[0] == userr.split('|')[1]:
                    self.response.out.write("welcome, %s!" %user.username)
                    return
        self.redirect("/blog/signup")
            

def valid_pw(name, pw, h):
    ###Your code here
    salt = h.split('|')[1]
    if h.split('|')[0] == hashlib.sha256(name + pw + salt).hexdigest():
        return True
    else:
        return False
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))
def make_pw_hash(name, pw):
    salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)