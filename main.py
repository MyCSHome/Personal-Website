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
import logging

html = """
<!DOCTYPE html>

<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""

def rot13(text):
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
    special = {'<' : '&lt;', '>' : '&gt;', '"': '&quot;', '&':'&amp;'}
    list = []
    for letter in text:
        if letter in lowercase:
            number = ord(letter)
            if number >= 110:
                number = 97 + number - 110
            else:
                number += 13
            list.append(chr(number))
        elif letter in uppercase:
            number = ord(letter)
            if number >= 78:
                number = 65 + number - 78
            else:
                number += 13
            list.append(chr(number))
        elif letter in special:
            list.append(special[letter])
        else:
            list.append(letter)
    return ''.join(list)
          
def gethtml(html,value):
    logging.info("bbb")
    return html % value

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(gethtml(html,""))
    def post(self):
        text = self.request.get('text')
        self.response.out.write(gethtml(html,rot13(text)))
    
        

app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
