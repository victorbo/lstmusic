#!/usr/bin/python
# -*- coding: utf-8 -*-
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
from google.appengine.ext import ndb
import cgi
import logging
import datetime
from google.appengine.datastore import datastore_query
import time

# ﻿sudo /home/farcot/devtools/google_appengine/appcfg.py --oauth2 update lstmusic.yaml  -V 1-2-6

class Greeting(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_book(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)


class MainPage(webapp2.RequestHandler):
    GREETINGS_PER_PAGE = 20

    def get(self):
        guestbook_name = self.request.get('guestbook_name')
        ancestor_key = ndb.Key('Book', guestbook_name or '*notitle*')
        greetings = Greeting.query_book(ancestor_key).fetch(
            self.GREETINGS_PER_PAGE)

        self.response.out.write('<html><body>')

        for greeting in greetings:
            self.response.out.write(
                '<blockquote>%s</blockquote>' % cgi.escape(greeting.content))

        self.response.out.write('</body></html>')


class List(webapp2.RequestHandler):
    GREETINGS_PER_PAGE = 10

    def get(self):
        """Handles requests like /list?cursor=1234567."""
        cursor = ndb.Cursor(urlsafe=self.request.get('cursor'))
        greets, next_cursor, more = Greeting.query().fetch_page(
            self.GREETINGS_PER_PAGE, start_cursor=cursor)

        self.response.out.write('<html><body>')

        for greeting in greets:
            self.response.out.write(
                '<blockquote>%s</blockquote>' % cgi.escape(greeting.content))

        if more and next_cursor:
            self.response.out.write('<a href="/list?cursor=%s">More...</a>' %
                                    next_cursor.urlsafe())

        self.response.out.write('</body></html>')


class FileSubItem(ndb.Expando):
    key          = ndb.StringProperty(indexed=True)
    type         = ndb.StringProperty(indexed=True)
    tag          = ndb.StringProperty(indexed=True)


class FileOutputItem(FileSubItem):
    status       = ndb.StringProperty(indexed=True)
    url          = ndb.StringProperty(indexed=False)
    secure       = ndb.BooleanProperty(indexed=False, default=False)


class FileOutput(ndb.Expando):
    items        = ndb.StructuredProperty(FileOutputItem, repeated=True)


class FileInput(ndb.Expando):
    items        = ndb.StructuredProperty(FileSubItem, repeated=True)



class File(ndb.Expando):
    # key is file_name
    # user is parent

    _default_indexed   = False
    date_updated       = ndb.DateTimeProperty(indexed=True)  # updating on create and explicit update
    date_created       = ndb.DateTimeProperty(indexed=False, auto_now_add=True)

    parent_folder_key  = ndb.KeyProperty(kind='Folder', indexed=True)
    file_name          = ndb.StringProperty(indexed=True)
    media_type         = ndb.StringProperty(indexed=True)
    tags               = ndb.StringProperty(indexed=True, repeated=True)
    labels             = ndb.StringProperty(indexed=True, repeated=True)
    # sites              = ndb.StringProperty(indexed=True, repeated=True)
    original_file_name = ndb.StringProperty(indexed=True)

    input              = ndb.StructuredProperty(FileInput)
    output             = ndb.StructuredProperty(FileOutput)

    @classmethod
    def query_file(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date_updated)


class BillingProperties(ndb.Model):
    last_updated = ndb.DateTimeProperty()
    stat_time = ndb.DateTimeProperty()


class FileList(webapp2.RequestHandler):
    FILES_PER_PAGE = 3

    # def get(self):
    #     start_cursor = self.request.get('cursor', None)
    #     logging.info("Cursor: %s" % start_cursor)
    #
    #     query = File.query()
    #     query = query.filter(File.media_type == 'secure_music')
    #
    #     #start_cursor = ndb.Cursor(urlsafe=self.request.get('cursor'))
    #     if start_cursor:
    #         start_cursor = datastore_query.Cursor.from_websafe_string(start_cursor)
    #
    #     files, next_cursor, more = query.fetch_page(self.FILES_PER_PAGE, start_cursor=start_cursor)
    #
    #     self.response.out.write('<html><body>')
    #
    #     for file_obj in files:
    #     #for i in range(10):
    #      #   file_obj = files[i]
    #         self.response.out.write(
    #             '<blockquote>%s</blockquote>' % cgi.escape(str(file_obj.to_dict())))
    #
    #     self.response.out.write("Next cursor: %s" % next_cursor.urlsafe())
    #
    #     # if more and next_cursor:
    #     #     self.response.out.write('<a href="/list?cursor=%s">More...</a>' %
    #     #                             next_cursor.urlsafe())
    #
    #     self.response.out.write('</body></html>')
    def get(self):
        start_cursor = self.request.get('cursor', None)

        mediatype = self.request.get('mediatype', 'picture')
        if mediatype is None:
            mediatype = 'picture'
        logging.info("mediatype: %s" % mediatype)
        query = File.query()
        query = query.filter(File.media_type == mediatype)

        # ------------------------------------------------------------------------------
        self.response.out.write('<html><head>')
        self.response.out.write('<script language="javascript" type="text/javascript">')
        self.response.out.write('function foo(){alert("call function foo()");}')
        self.response.out.write('</script>')
        self.response.out.write('</head><body>')		
        self.response.out.write('<table style="width:1400px;border:1px solid black;margin:0 auto;">')
        self.response.out.write('<tr>')
        self.response.out.write('<th style="width:20%;">"file_name"</th>')
        self.response.out.write('<th style="width:70%;">"file_url"</th>')
        self.response.out.write('<th style="width:10%;">"file_size"</th>')
        self.response.out.write('</tr>')
         # ------------------------------------------------------------------------------
          
        # start_cursor = ndb.Cursor(urlsafe=self.request.get('cursor'))
        if start_cursor:
            start_cursor = datastore_query.Cursor.from_websafe_string(start_cursor)

        files, next_cursor, more = query.fetch_page(self.FILES_PER_PAGE, start_cursor=start_cursor)
        logging.debug("number of files: %s" % len(files))
        self.draw_answ(files)

        while more:
            files, next_cursor, more = query.fetch_page(self.FILES_PER_PAGE, start_cursor=next_cursor)
            logging.debug("number of files: %s" % len(files))
            self.draw_answ(files)

        # if more and next_cursor:
        #     self.response.out.write('<a href="/list?cursor=%s">More...</a>' %
        #                             next_cursor.urlsafe())

        self.response.out.write('</body></html>')
        logging.info("finish GET function")

    def draw_answ(self, files):
        logging.info("func draw_answ files: %s" % files)
        for file_obj in files:
            logging.info("Type of file_obj: %s" % type(file_obj))
            raw = file_obj.to_dict()
            logging.info("Type of raw %s" % type(raw))
            logging.info("raw object after function (to_dict): %s" % raw)

            logging.info("number of fields = %s" % len(raw.keys()))
            logging.info("fields = %s" % str(raw.keys()))
            for i_col in raw.keys():
                logging.info("key = %s -----  value = %s" % (i_col, raw[i_col] if raw[i_col] is not None else 'None'))
            for prop_key, prop_val in raw.iteritems():
                logging.info("prop_key: %s prop_val: %s" % (prop_key, prop_val))
            file_name = raw['original_file_name']
            file_url = raw['file_url']
            file_size = str(raw['file_size'])
            self.response.out.write('<tr style="background-color:#f0ffff">')
            self.response.out.write('<td style="width:20%s;overflow:hidden;text-overflow:ellipsis;" title="%s">\
                                    <a href="#" onClick="foo();">%s%s' % ('%;', file_name, file_name, '</a></td>'))
            self.response.out.write('<td style="width:70%s;overflow:hidden;text-overflow:ellipsis;"\
                                    title="%s">%s%s' % ('%;', file_url, file_url, '</td>'))
            self.response.out.write('<td style="width:10%s">%s%s' % ('%;', file_size, '</td>'))
            self.response.out.write('</tr>')
        

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # billing_periods = BillingProperties()
        # billing_periods.stat_time = datetime.datetime.utcnow()
        # billing_periods.last_updated = datetime.datetime.utcnow()
        # billing_periods.put()
        period_key = ndb.Key('BillingProperties', "UsersStats15")
        res = period_key.get()
        logging.info("Result of get: %s" % str(res))
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/list', FileList)
], debug=True)
