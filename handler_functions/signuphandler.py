import webapp2
import re
import cgi
from main import jinja_environment
from google.appengine.ext import db
import hashlib
import random
import string

class User(db.Model):
    username = db.StringProperty(required = True)
    encryption = db.StringProperty(required = True)
    mailbox = db.StringProperty()


class SignupHandler(webapp2.RequestHandler):
    e1 = "That's not a valid username."
    e2 = "That wasn't a valid password."
    e3 = "Your passwords didn't match."
    e4 = "That's not a valid email."
    e5 = "That user already exists."
    USER = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASSWORD = re.compile(r"^.{3,20}$")
    EMAIL = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    def get(self):
        dic = {"username" : "", "email" : "", "name_e" : "", "pass_e":"", "email_e":"", "veri_e":""} 
        html = jinja_environment.get_template('signup.html')
        self.response.out.write(html.render(dic))

    def post(self):
        u = self.request.get('username')
        p1 = self.request.get('password')
        p2 = self.request.get('verify')
        e = self.request.get('email')
        user = valid_username(u)
        password = valid_password(p1)
        email = valid_email(e)
        verify = self.same_password(p1,p2)
        existing = db.GqlQuery("select * from User where username =:1" , u)
        if user and password and email and verify and not existing.get():
            encryption = make_pw_hash(u, p1)
            newuser = User(username = u, encryption = encryption, mailbox = e )
            newuser.put()
            userid = newuser.key().id()
            self.response.headers.add_header('Set-Cookie', 'user_id=%s|%s;Path=/' % (userid,encryption.split('|')[0]))
            self.redirect("/signup/welcome")
        else:
            dic = {}
            dic["username"] = cgi.escape(u, quote = True)
            dic["email"] = cgi.escape(e, quote = True)
            if not user:
                dic["name_e"]=self.e1
            else:
                dic["name_e"]=""
            if existing.get():
                dic["name_e"]=self.e5
            if not email:
                dic["email_e"]=self.e4
            else:
                dic["email_e"]=""
            if not password:
                dic["pass_e"] = self.e2
                dic["veri_e"] = ""
            else:
                dic["pass_e"]=""
                if not verify:
                    dic["veri_e"] = self.e3
                else:
                    dic["veri_e"] = ""
            html = jinja_environment.get_template('signup.html')
            self.response.out.write(html.render(dic))
    def same_password(self, p1, p2):
            return p1 == p2
            
            
def valid_username(username):
    return SignupHandler.USER.match(username)
def valid_password(password):
    return SignupHandler.PASSWORD.match(password)
def valid_email(email):
    return SignupHandler.EMAIL.match(email) or email == ""

    
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))
def make_pw_hash(name, pw):
    salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)
