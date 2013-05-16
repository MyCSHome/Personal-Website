import webapp2
import re
import cgi
from main import jinja_environment

class SignupHandler(webapp2.RequestHandler):
    e1 = "That's not a valid username."
    e2 = "That wasn't a valid password."
    e3 = "Your passwords didn't match."
    e4 = "That's not a valid email."
    USER = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASSWORD = re.compile(r"^.{3,20}$")
    EMAIL = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    def get(self):
        dic = {"username" : "", "email" : "", "name_e" : "", "pass_e":"", "email_e":"", "veri_e":""} 
        html = jinja_environment.get_template('signup.html')
        self.response.out.write(html.render(dic))
    def valid_username(self, username):
        return self.USER.match(username)
    def valid_password(self, password):
        return self.PASSWORD.match(password)
    def valid_email(self, email):
        return self.EMAIL.match(email) or email == ""
    def same_password(self,p1, p2):
        return p1 == p2
    def post(self):
        u = self.request.get('username')
        p1 = self.request.get('password')
        p2 = self.request.get('verify')
        e = self.request.get('email')
        user = self.valid_username(u)
        password = self.valid_password(p1)
        email = self.valid_email(e)
        verify = self.same_password(p1,p2)
        if user and password and email and verify:
            self.redirect("/signup/welcome?username=%s" % u)
        else:
            dic = {}
            dic["username"] = cgi.escape(u, quote = True)
            dic["email"] = cgi.escape(e, quote = True)
            if not user:
                dic["name_e"]=self.e1
            else:
                dic["name_e"]=""
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