##
# This file is part of agithub
# Originally created by Jonathan Paugh
#
# https://github.com/jpaugh/agithub
#
# Copyright 2012 Jonathan Paugh
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
##
"""
Interface to GitHub.

@author: Jonathan Paugh
@uathor: Jens Timmerman (Ghent University)
@uathor: Kenneth Hoste (Ghent University)
"""

import base64
import re
import httplib, urllib
try:
    import json
except ImportError:
    import simplejson as json

from vsc import fancylogger


class Client(object):
  http_methods = (
      'get',
      'post',
      'delete',
      'put',
      )

  def __init__(self, username=None, password=None, token=None):
    self.auth_header = None
    if username is not None:
      if password is None and token is None:
        raise TypeError("You need a password or an OAuth token to authenticate as " + username)
      if password is not None and token is not None:
        raise TypeError("You cannot use both password and OAuth token authenication")

      if password is not None:
        self.auth_header = self.hash_pass(password)
      elif token is not None:
        self.auth_header = 'Token %s' % token
    self.username = username

  def get(self, url, headers={}, **params):
    url += self.urlencode(params)
    return self.request('GET', url, None, headers)

  def delete(self, url, headers={}, **params):
    url += self.urlencode(params)
    return self.request('DELETE', url, None, headers)

  def post(self, url, body=None, headers={}, **params):
    url += self.urlencode(params)
    return self.request('POST', url, json.dumps(body), headers)

  def put(self, url, body=None, headers={}, **params):
    url += self.urlencode(params)
    return self.request('PUT', url, json.dumps(body), headers)

  def request(self, method, url, body, headers):
    if self.auth_header is not None:
        headers['Authorization'] = self.auth_header
    headers['User-Agent'] = 'agithub'
    fancylogger.getLogger().debug('cli request: %s, %s, %s %s', method, url, body, headers)
    #TODO: Context manager
    conn = self.get_connection()
    conn.request(method, url, body, headers)
    response = conn.getresponse()
    status = response.status
    body = response.read()
    try:
      pybody = json.loads(body)
    except ValueError:
      pybody = body
    fancylogger.getLogger().debug('reponse len: %s ', len(pybody))
    conn.close()
    return status, pybody

  def urlencode(self, params):
    if not params:
      return ''
    return '?' + urllib.urlencode(params)

  def hash_pass(self, password):
    return 'Basic ' + base64.b64encode('%s:%s' % (self.username, password)).strip()

  def get_connection(self):
    return httplib.HTTPSConnection('api.github.com')


class Github(object):
  '''The agnostic Github API. It doesn't know, and you don't care.
  >>> from agithub import Github
  >>> g = Github('user', 'pass')
  >>> status, data = g.issues.get(filter='subscribed')
  >>> data
  ... [ list_, of, stuff ]
  >>> status, data = g.repos.jpaugh64.repla.issues[1].get()
  >>> data
  ... { 'dict': 'my issue data', }
  >>> name, repo = 'jpaugh64', 'repla'
  >>> status, data = g.repos[name][repo].issues[1].get()
  ... same thing
  >>> status, data = g.funny.I.donna.remember.that.one.get()
  >>> status
  ... 404

  That's all there is to it. (blah.post() should work, too.)

  NOTE: It is up to you to spell things correctly. Github doesn't even
  try to validate the url you feed it. On the other hand, it
  automatically supports the full API--so why should you care?
  '''
  def __init__(self, *args, **kwargs):
    self.client = Client(*args, **kwargs)
  def __getattr__(self, key):
    return RequestBuilder(self.client).__getattr__(key)

class RequestBuilder(object):
  '''RequestBuilder(client).path.to.resource.method(...)
      stands for
  RequestBuilder(client).client.method('path/to/resource, ...)

  Also, if you use an invalid path, too bad. Just be ready to catch a
  You can use item access instead of attribute access. This is
  convenient for using variables' values and required for numbers.
  bad status from github.com. (Or maybe an httplib.error...)

  To understand the method(...) calls, check out github.client.Client.
  '''
  def __init__(self, client):
    self.client = client
    self.url = ''

  def __getattr__(self, key):
      def partial(func, *args, **keywords):
          def newfunc(*fargs, **fkeywords):
              newkeywords = keywords.copy()
              newkeywords.update(fkeywords)
              return func(*(args + fargs), **newkeywords)
          newfunc.func = func
          newfunc.args = args
          newfunc.keywords = keywords
          return newfunc

      if key in self.client.http_methods:
          mfun = getattr(self.client, key)
          fun = partial(mfun, url=self.url)
          return fun
      self.url += '/' + str(key)
      return self

  __getitem__ = __getattr__

  def __str__(self):
    '''If you ever stringify this, you've (probably) messed up
    somewhere. So let's give a semi-helpful message.
    '''
    return "I don't know about " + self.url

  def __repr__(self):
    return '%s: %s' % (self.__class__, self.__str__())

