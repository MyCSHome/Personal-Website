import webapp2


class LogoutHandler(webapp2.RequestHandler):


    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=;Path=/')
        self.redirect("/signup")

    

