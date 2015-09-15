#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.cookiejar import CookieJar
from html.parser import HTMLParser
from urllib.parse import urlencode, parse_qs
from urllib.request import Request, build_opener, HTTPRedirectHandler, \
                           HTTPCookieProcessor # HTTPRedirectHandler?
from getpass import getpass

class AuthParams(dict):
    
    def __init__(self, client_id='4805647',
            scope='notify,friends,photos,audio,video,docs,notes,'
                  'pages,status,wall,groups,messages,email,'
                  'notifications,stats,ads,offline',
            display='mobile', 
            response_type='token',
            v='5.37', # Vk API version
            redirect_uri='https://oauth.vk.com/blank.html'):
            
        paramsDict = {'client_id' : client_id, 'scope': scope,
                'display': display, 'response_type': response_type,
                'v': v, 'redirect_uri': redirect_uri}
        dict.__init__(self, paramsDict)

    def getAuthURL(self):
        authurl = 'https://oauth.vk.com/authorize'
        params = urlencode(self)   #'&'.join(key+'='+self[key] for key in self)
        return authurl+'?'+params
             
class AuthFormParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.url = None
        self.params = {}
        self.in_form = False
        self.form_parsed = False
        self.method = "GET"

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "form":
            if self.form_parsed:
                raise RuntimeError("Second form on page")
            if self.in_form:
                raise RuntimeError("Already in form")
            self.in_form = True 
        if not self.in_form:
            return
        attrs = dict((name.lower(), value) for name, value in attrs)
        if tag == "form":
            self.url = attrs["action"] 
            if "method" in attrs:
                self.method = attrs["method"]
        elif tag == "input" and "type" in attrs and "name" in attrs:
            if attrs["type"] in ["hidden", "text", "password"]:
                self.params[attrs["name"]] = \
                                    attrs["value"] if "value" in attrs else ""

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "form":
            if not self.in_form:
                raise RuntimeError("Unexpected end of <form>")
            self.in_form = False
            self.form_parsed = True

    def clear(self):
        self.url = None
        self.params = {}
        self.in_form = False
        self.form_parsed = False
        self.method = "GET"


def auth(email, password, 
         user_agent='Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0)'
                                            ' Gecko/20100101 Firefox/39.0'):
    """Portable and quick emulator of brouser for Vk API authorisation."""
    user_agent = ('User-Agent', user_agent)
    opener = build_opener(HTTPCookieProcessor(CookieJar()))
    parser = AuthFormParser()
    request = Request(AuthParams().getAuthURL())
    request.add_header(*user_agent)

    parser.feed(opener.open(request).read().decode('utf8'))
    request = Request(parser.url)
    request.add_header(*user_agent)

    if 'email' in parser.params and "pass" in parser.params:
        parser.params["email"] = email
        parser.params["pass"] = password
        data = urlencode(parser.params).encode('ascii')
        parser.clear()
        parser.feed(opener.open(request, data).read().decode('utf8'))
        request = Request(parser.url)
        request.add_header(*user_agent)
    data = urlencode(parser.params).encode('ascii')

    return parse_qs(opener.open(request, data).geturl().split('#')[1])

def getlogin():
    return (input('email> '), getpass('pass> '))

if __name__ == '__main__':
    # Добавить обработку параметров командной строки
    data = auth(*getlogin())
    for key in data:
        print('{0: <{2}}: {1}'.format(key, data[key], 
                                      max(len(k) for k in data)))
        
