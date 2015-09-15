#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import vk.auth
import vk.api
import json
import sys
import os
import argparse
from urllib.request import urlopen, Request
from getpass import getpass
from hashlib import md5
import string

def createParser():
    parser = argparse.ArgumentParser(prog='vkmusicdumper.py')
    parser.add_argument('-p', '--password', nargs='?', default = '')
    parser.add_argument('-e', '--email', nargs='?', default = '')
    parser.add_argument('-d', '--dir', nargs='?', default = '')
    parser.add_argument('-t', '--token', nargs='?', default = '')
    parser.add_argument('-a', '--auto', action='store_true')
    parser.add_argument('-m', '--mute', action='store_true')
    return parser
    
def condprint(mute, text, end='\n')
    if not mute:
        print(text, end=end)

def main(email, password, dir='.', auto=False, mute=False):
    # Переименовать функцию
    # Убрать аутентификацию
    # Разбить на подфункции
    condprint(mute, 'Authentification: ', end='')
    access_token = vkauth.auth(email, password)['access_token'][0]
    condprint(mute, 'success')
    condprint(mute, 'Request playlist: ', end='')
    answer = api.apicall('audio.get', '', access_token)
    condprint(mute, 'success')
    
    with open(os.path.join(dir, 'audio.get.json'), 'w', encoding='utf8') as f:
        json.dump(answer, f, indent='    ', 
                  ensure_ascii=False, sort_keys=True)
    playlist = answer['response']
    count =  len(playlist)
    counter = count+1

    
    hashdict = {}
    failslist = []
    duplicatesdict = []
    
# Добавить логи ошибок загрузки и дубликатов    
# Добавить подгрузку lyrics
# Добавить лог с отношением хешей к парам (артист, название)
    for filename in [path for path in os.listdir(dir) 
                                   if os.path.isfile(path)]:
        m = md5()
        with open(os.path.join(dir,filename), 'rb') as file:
            filedata = file.read()
            m.update(filedata)
            hash = m.hexdigest
            size = len(filedata)
        hashdict[(hash,size)] = filename

    for track in playlist:
        nexttrack = False
        counter -= 1
        req = Request(dict['url'])
        req.add_header('User-Agent', '')
        filename = '{0[artist]:.32} - {0[title].32}.mp3'.format(track).replace('/','_').replace('\\','_').replace('?','_').replace('*','_').replace(':','_').replace('"','_').replace('|','_').replace('<','_').replace('>','_')

        condprint(mute, '#%d/%d, %s:  ' % \
                        ((count-counter)+1,count,filename), end='')
            
# Проверить файл с таким именем на наличие в папке

        try:
            file = urlopen(req).read()
        except:
            #тут записать ошибку в лог
            condprint(mute, '\tFailed to get file')
            continue
        
        m = md5()
        m.update(file)
        hash = m.hexdigest()
        size = len(file)
        
        if (hash, size) in hashdict:
            for fn in hashdict[(hash, size)]:
                with open(os.path.join(dir,fn)) as f:
                    if f.read() == file:
                        print('\n\tDuplicate of: %s'%(hashdict[(hash, size)]))
                        nexttrack = True
                        break
            else:                
                hashdict[(hash, size)].append(filename)
                #тут
        else: 
            hashdict[(hash, size)] = [filename]
            #и здесь реализовать запись в лог
                
        if nexttrack:
            continue
        
        with open(os.path.join(dir, filename), 'wb') as f:
            f.write(file)
        if not mute:
            print('Saved')
            
        
    if not mute:
        print('Done.')
    if not auto:
        input('Press enter> ')
        
if __name__ == '__main__':
    argparser = createParser()
    args = argparser.parse_args()

    if ((not args.email) or (not args.password)) and args.auto:
        raise IOError('have no email and password in auto mode')
    if not args.email:
        args.email = input('email> ')
    if not args.password:
        args.password = getpass('password> ')


    while not os.path.isdir(args.dir):
        if os.path.isfile(args.dir):
            if args.auto:
                raise IOError('given path is file')
            else:
                print('Wrong pathname for saving directory!')
                args.dir = input('Directory to save> ')
        elif not args.dir:
            if args.auto:
                args.dir == '.'
            else:
                args.dir = input('Directory to save> ')
        else:            
            os.makedirs(args.dir)
            
    main(args.email, args.password, args.dir, args.auto, args.mute)
            
    

    
    
    

