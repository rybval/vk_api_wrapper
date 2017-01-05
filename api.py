#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen, Request
from urllib.parse import urlencode, parse_qs
from json import loads
import time

__all__ = ('API_VERSION', 'MAX_CALLS_PER_SECOND', 'MIN_PAUSE_BETWEEN_CALLS',
           'doc_types', 'timeout', 'call')

API_VERSION = '5.37'
MAX_CALLS_PER_SECOND = 3
MIN_PAUSE_BETWEEN_CALLS = (1/MAX_CALLS_PER_SECOND)*1.02

doc_types = (None, "текстовый документ", "архив", "gif", "изображение",
             "аудио", "видео", "электронная книга", "неизвестно")

def timeout(last_call_time=None):
    """
    Waits enough time to not let server throw
    'too many requests per second' error.
    """
    if last_call_time is None:
        last_call_time = time.time()
    time_to_sleep = MIN_PAUSE_BETWEEN_CALLS - (time.time() - last_call_time)
    if time_to_sleep > 0:
        time.sleep(time_to_sleep)

def call(method, user_agent='', **params):
    """ Any method from Vk API can be called, using this function """
    if 'v' not in params:
        params['v'] = API_VERSION
    url = 'https://api.vk.com/method/{0}?{1}'.format(method, urlencode(params))
    req = Request(url)
    req.add_header('User-Agent', user_agent)
    resp = urlopen(req)
    dictionary = loads(resp.read().decode())
    if 'error' in dictionary.keys():
        raise Exception(dictionary['error'], url)
    elif 'response' not in dictionary.keys():
# need refactor
        raise Exception('Something wrong')
    else:
        return dictionary['response']

if __name__ == '__main__':
    method = input('Type API method title (example: utils.getServerTime)> ')
    params = input('Type params string (or just press "Enter")> ')
    pdict = parse_qs(params)
    for key in pdict.keys():
        pdict[key] = ''.join(pdict[key])
    print('Trying call', method,'...')
    try:
        response = call(method, **pdict)
    except Exception as ex:
        print('\tfail: {0}'.format(ex))
    else:
        print('\tsuccess, response =', response)
