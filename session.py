# -*- coding: utf-8 -*-

from vk.auth import auth
from vk.api import call
from datetime import datetime, timedelta
from functools import partial

class Session:
    def __init__(self, client_id=None, scope=None, 
                 email=None, password=None, access_token=None):
        self.access_token = None
        #self.user_id = None
        self.expire_time = None
                 
        if access_token:
            self.access_token = access_token
        elif client_id and scope and email and password:
            self.auth(client_id, scope, email, password)

    def auth(self, client_id, scope, email, password):
        response = auth(client_id, scope, email, password)
        if 'error' in response:
            raise Exception(response['error_description'])
        self.access_token = response['access_token'][0]
        #self.user_id = int(response['user_id'][0])
        if 'expires_in' in response:
            self.expire_time = (datetime.now() + 
                           timedelta(seconds = int(response['expires_in'][0])))
        else:
            self.expire_time = 'infinity'
    
    def call(self, method, **kwargs):
        if self.access_token:
            return call(method, access_token = self.access_token, **kwargs)
        else:
            return call(method, **kwargs)
    
    def __getattr__(self, method_prefix):
        return _getattrgate(self, method_prefix)
        
    def __call__(self, method, **kwargs):
        return self.call(method, **kwargs)
        
class _getattrgate:
    def __init__(self, session, method_prefix):
        self.session = session
        self.method_prefix = method_prefix
        
    def __getattr__(self, method_suffix):
        return partial(self.session.call, self.method_prefix+'.'+method_suffix)
        