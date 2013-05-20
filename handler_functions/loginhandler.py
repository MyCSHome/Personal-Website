import webapp2
import re
import cgi
from main import jinja_environment
from google.appengine.ext import db
import hashlib
import random
import string
from signuphandler import User

class LoginHandler(webapp2.RequestHandler):
    e1 = "The user does not exist!"
    e2 = "incorrect password!"

    def get(self):
        dic = {"e1" : ""} 
        html = jinja_environment.get_template('login.html')
        self.response.out.write(html.render(dic))

    def post(self):
        u = self.request.get('username')
        p1 = self.request.get('password')
        existing = db.GqlQuery("select * from User where username =:1" , u)
        user = existing.get()
        if user:
            salt= user.encryption.split('|')[1]
            if make_pw_hash(u, p1, salt) == user.encryption:
                id = str(user.key().id())
                encryption = str(user.encryption.split('|')[0])
                self.response.headers.add_header('Set-Cookie', 'user_id=' +id+'|'+encryption+';Path=/')
                self.redirect("/signup/welcome")
            else:
                dic = {}
                dic["e1"] = LoginHandler.e2
                html = jinja_environment.get_template('login.html')
                self.response.out.write(html.render(dic))
        else:
            dic = {}
            dic["e1"] = LoginHandler.e1
            html = jinja_environment.get_template('login.html')
            self.response.out.write(html.render(dic))

            
def valid_pw(name, pw, h):
    ###Your code here
    salt = h.split('|')[1]
    if h.split('|')[0] == hashlib.sha256(name + pw + salt).hexdigest():
        return True
    else:
        return False
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))
def make_pw_hash(name, pw, salt=""):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)
