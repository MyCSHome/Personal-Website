import webapp2
from main import jinja_environment
from tool_functions.rot13 import rot13

class Rot13Handler(webapp2.RequestHandler):
    def get(self):
        dic = {"value" : ""}
        html = jinja_environment.get_template('rot.html')
        self.response.out.write(html.render(dic))
    def post(self):
        text = self.request.get('text')
        dic = {"value" : rot13(text)}
        html = jinja_environment.get_template('rot.html')
        self.response.out.write(html.render(dic))