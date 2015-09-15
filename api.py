#!/usr/bin/env python3

from urllib.request import urlopen, Request
from urllib.parse import urlencode
from json import loads

def call(method, params={}, access_token=None, v='5.37', user_agent=''):
    """ Any method from Vk API can be called, using this function """
    if 'v' not in params:
        params['v'] = v
    if access_token and 'access_token' not in params:
        params['access_token'] = access_token
    url = 'https://api.vk.com/method/{0}?{1}'.format(method, urlencode(params))
    req = Request(url)
    req.add_header('User-Agent', user_agent)
    resp = urlopen(req)
    dictionary = loads(resp.read().decode())
    if 'error' in dictionary.keys():
        raise Exception(dictionary['error'], url)
    elif 'response' not in dictionary.keys():
        raise Exception('Something wrong')
    else:
        return dictionary['response']