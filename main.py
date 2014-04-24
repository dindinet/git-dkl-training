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
import os
import sys
import urllib
from wsgiref.handlers import CGIHandler
from google.appengine.ext.webapp import template
import cgi
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import mail


class MainHandler(webapp.RequestHandler):

    def get(self):
            xform_content = ""
              form_content =    "<form action=\"/phorm\" method=\"post\">"
              form_content = form_content +   "<table cellpadding=\"10px\" border=\"0\" style=\"font-size: 13px; font-family: Tahoma, Verdana;\">"
              form_content = form_content +   "<tr> <td align=\"right\">Your Name : </td> <td><input name=\"ph_name\" type=\"text\" style=\"width: 250px;\" /></td> </tr>"
              form_content = form_content +   "<tr> <td align=\"right\">Your Email : </td> <td><input name=\"ph_email\" type=\"text\" style=\"width: 250px;\" /></td> </tr>"
              form_content = form_content +   "<tr> <td align=\"right\">Subject : </td> <td><input name=\"ph_subject\" type=\"text\" style=\"width: 250px;\" /></td> </tr>"
              form_content = form_content +   "<tr> <td align=\"right\" valign=\"top\">Message : </td> <td><textarea rows=\"10\" cols=\"40\" name=\"ph_message\" style=\"font-size: 13px; padding: 3px; font-family: Tahoma, Verdana;\"></textarea></td> </tr>"
              form_content = form_content +   "<tr><td></td><td><input type=\"submit\" value=\"Submit\" class=\"submit\"/></td></tr>"
              form_content = form_content +   "</table>"
              form_content = form_content +   "</form>"
              template_values = {
               'content': form_content,
              }

              path = os.path.join(os.path.dirname(__file__), '_base.html')
              self.response.out.write(template.render(path, template_values))

class phormhandler(webapp.RequestHandler):

        def post(self):
        
            s_name =(cgi.escape(self.request.get('ph_name')))
            s_email =(cgi.escape(self.request.get('ph_email')))
            s_subject =(cgi.escape(self.request.get('ph_subject')))
            s_message =(cgi.escape(self.request.get('ph_message')))
            
            contactphorm = mail.EmailMessage(sender="Krav Maga Blogger <dklongley@gmail.com>", subject= "Contact Form on Krav Maga Blogger")
            contactphorm.to = "Dave Longley <dklongley@gmail.com>"
            
            g_body = "<table>"
            g_body = g_body + "<tr><td>name: </td><td>" + s_name + "</td><tr>"
            g_body = g_body + "<tr><td>email: </td><td>" + s_email + "</td><tr>"
            g_body = g_body + "<tr><td>subject: </td><td>" + s_subject + "</td><tr>"
            g_body = g_body + "<tr><td>message: </td><td>" + s_message + "</td><tr>"
            g_body = g_body + "</table>"
            
            contactphorm.html = g_body
            
            contactphorm.send()
            
            
            form_response = "<div> Thanks " + s_name + " we have received your message and will respond soon.</div>"
            template_values = {
        'content': form_response,
      }

            path = os.path.join(os.path.dirname(__file__), '_base.html')
            self.response.out.write(template.render(path, template_values))
            
class gcohandler(webapp.RequestHandler):

    def post(self):
        GC_Notification = cgi.FieldStorage()
            
        g_body = "<table>"
        for name in GC_Notification.keys():
            g_body = g_body + "<tr><td>" + name +": </td><td>" + urllib.unquote(GC_Notification[name].value) + "</td><tr>"

        g_body = g_body + "</table>"
            
        gco_notification = mail.EmailMessage(sender="GCO handler <dklongley@gmail.com>", subject= " - Google Checkout Notification") 
        gco_notification.to = "Dave Longley <dklongley@gmail.com>"
            
        gco_notification.html = g_body
            
        gco_notification.send()
        
        self.response.out.write("<notification-acknowledgment xmlns=\"http://checkout.google.com/schema/2\" serial-number=\"" + GC_Notification["serial-number"].value + "\"/>")


class prophandler(webapp.RequestHandler):
    
    def get(self):
      
      
      gd_client = gdata.spreadsheet.service.SpreadsheetsService()
      gdata.alt.appengine.run_on_appengine(gd_client,store_tokens=False, single_user_mode=True)# remember this is required on app engine when in single user mode.
      #gdata.alt.appengine.run_on_appengine(gd_client._GetDocsClient())
      #gdata.alt.appengine.run_on_appengine(gd_client._GetSpreadsheetsClient())
      
      gd_client.email = 'dklongley@gmail.com'
      gd_client.password = 'G5tgbM0okm'
      gd_client.source = 'phorm-handler'

      try:                    
      # log in
        gd_client.ProgrammaticLogin()
      except socket.sslerror, e:
        logging.error('Spreadsheet socket.sslerror: ' + str(e))
        return False
        
        
      key = "t4-pJI7rW8_Y5H7hhPpQ-IA"
      #key =(cgi.escape(self.request.get('k')))
      wksht_id = "od6"
      
      #wksht_id =(cgi.escape(self.request.get('w')))
      q = gdata.spreadsheet.service.ListQuery()
      q.orderby = 'column:Price'
      q.reverse = 'false'

      # Here's the actual query
      #if from_date and to_date:
        #q.sq = 'timestamp >= %s and timestamp <= %s' % (from_date, to_date)
      #elif from_date:
        #q.sq = 'timestamp >= %s' % from_date
      #elif to_date:
        #q.sq = 'timestamp <= %s' % to_date

      try:
      # fetch the spreadsheet data
        feed = gd_client.GetListFeed(key, wksht_id)
      except gdata.service.RequestError, e:
        logging.error('Spreadsheet gdata.service.RequestError: ' + str(e))
        return False
      except socket.sslerror, e:
        logging.error('Spreadsheet socket.sslerror: ' + str(e))
        return False
      # Iterate over the rows
      prophtml = ""
      
      for row_entry in feed.entry:
        # to get the column data out, you use the text_db.Record class, then use the dict record.content
        record = gdata.spreadsheet.text_db.Record(row_entry=row_entry)
        prophtml = prophtml + "<div class=\"property\">"
        prophtml = prophtml + "Property Ref:" + record.content['ref'] +"<br/>"
        prophtml = prophtml + "Price:" + record.content['price'] +"<br/>"
        prophtml = prophtml + "Type:" + record.content['type'] +"<br/>"
        prophtml = prophtml + "Kind" + record.content['rubrum'] +"<br/>"
        prophtml = prophtml + "Location:" + record.content['location'] +"<br/>"
        prophtml = prophtml + "Pool:" + record.content['pool'] +"<br/>"
        prophtml = prophtml + "</div>"

      self.response.out.write("<div class=\"AllProperties\">" + prophtml + "</div><!-- END All Properties-->")
                                
                                
                                
  class dropboxer(webapp.RequestHandler):        
  

    
  def get(self,wealth):
    #Is the file on dropbox
    #dbfilename = self.request.uri.split("/")[-1]
    dbfilename = self.request.uri.replace('http://dkl-training.appspot.com/drop/','')
    #targeturl = "http://dl.dropbox.com/u/4577789/" + dbfilename
    targeturl = "http://www.maxgoldhouse.com/" + dbfilename
    result = urlfetch.fetch(targeturl)
    if result.status_code == 200:
            self.response.headers['Content-Type'] = getContentType(dbfilename)
      self.response.out.write(result.content.replace('href="http://www.maxgoldhouse.com/','href="http://dkl-training.appspot.com/drop/'))
    elif result.status_code != 200:
         Err(404)   

def getContentType( filename ): # lists and converts supported file extensions to MIME type
 ext = filename.split('.')[-1].lower()
 if ext == 'jpg' or ext == 'jpeg': return 'image/jpeg'
 if ext == 'png': return 'image/png'
 if ext == 'gif': return 'image/gif'
 if ext == 'doc': return 'application/msword'
 if ext == 'pdf': return 'application/pdf'
 if ext == 'xls': return 'application/vnd.ms-excel'
 if ext == 'pps': return 'application/vnd.ms-powerpoint'
 if ext == 'js': return 'application/x-javascript'
 if ext == 'zip': return 'application/zip'
 if ext == 'mp3': return 'audio/mpeg'
 if ext == 'html': return 'text/html'
 if ext == 'htm': return 'text/html'
 if ext == 'asp': return 'text/html'
 if ext == 'aspx': return 'text/html'
 if ext == 'php': return 'text/html'
 if ext == 'txt': return 'text/plain'
 if ext == 'css': return 'text/css'
 if ext == 'svg': return 'image/svg+xml'
 return 'text/html'
         
         
def Err(code, msg='Error'):
  """Renders an error to the browser (for non-webhandler situations)."""
  def DoErr(environ, start_response):
    """This function is passed to CGIHandler to render the http response."""
    start_response(str(code) + ' ' + msg, [('Content-type', 'text/html')])
    return ['<html><body>' + msg + '</body></html>']
  CGIHandler().run(DoErr)
    

application = webapp.WSGIApplication(
                                     [('/main', MainHandler),
                                      ('/phorm', phormhandler),
                                      ('/drop/(.*)', dropboxer),
                                      ('/prop', prophandler),
                                      ('/GCO', gcohandler)],
                                     debug=True)

def main():
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()