#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os


jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        main_page = jinja_environment.get_template('mainpage.html')
        self.response.out.write(main_page.render())
    

app = webapp2.WSGIApplication([('/', MainHandler),
('/blog/newpost', 'handler_functions.newbloghandler.NewBlogHandler'),
('/blog/flush', 'handler_functions.flushhandler.FlushHandler'),
('/blog/?(?:\.json)?', 'handler_functions.bloghandler.BlogHandler'),
('/rot13', 'handler_functions.rot13handler.Rot13Handler'),
('/blog/signup', 'handler_functions.signuphandler.SignupHandler'), 
('/blog/login', 'handler_functions.loginhandler.LoginHandler'),
('/blog/logout', 'handler_functions.logouthandler.LogoutHandler'),
('/blog/(\d+)(?:\.json)?', 'handler_functions.linkhandler.LinkHandler'),
('/blog/signup/welcome', 'handler_functions.thankshandler.ThanksHandler')], 
debug=True)
