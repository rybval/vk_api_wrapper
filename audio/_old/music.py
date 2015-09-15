#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from vk.auth import auth
from vk.api import apicall
from json import load, loads, dump, dumps
from os.path import join, isdir, isfile
from os import listdir, makedirs
import argparse
from urllib.request import urlopen, Request
from getpass import getpass
from hashlib import md5
import string
import sqlite3

# Воткнуть функции:
#    Сохранения аудио в папку
#    Сохранения аудио в бд sqlite
# Сохранять вместе со всеми метаданными и с текстами песен

def createParser():
    parser = argparse.ArgumentParser(prog='vkmusicdumper.py')
    parser.add_argument('-t', '--token', nargs='?', default = '')
    parser.add_argument('-p', '--password', nargs='?', default = '')
    parser.add_argument('-e', '--email', nargs='?', default = '')
    parser.add_argument('-d', '--dir', nargs='?', default = '')
    parser.add_argument('-a', '--auto', action='store_true')
    parser.add_argument('-m', '--mute', action='store_true')
    return parser
    
# def createAudioDB(path='.'):
    # c.execute('CREATE TABLE audio (id INTEGER,
                                    # vk_audio_id INTEGER,
                                    # vk_artist TEXT,
                                    # vk_title TEXT,
                                    # vk_genre_id INTEGER,
                                    # vk_uploader_id INTEGER,
                                    # vk_duration INTEGER,
                                    # vk_date_added INTEGER,
                                    # mp3_id INTEGER,
                                    # vk_uploader_id INTEGER)')
    
    
def condprint(mute, text, end='\n')
    if not mute:
        print(text, end=end)
        
def getAudio(access_token, owner_id=None, album_id=None):
    '''Это вообще нужно хардкодить?'''
    params = {}
    if owner_id:
        params['owner_id'] = owner_id
    if album_id:
        params['album_id'] = album_id
    return apicall('audio.get', params, access_token)
    
    
    
    with open(join(dir, 'audio.get.json'), 'w', encoding='utf8') as f:
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
    for filename in [path for path in listdir(dir) 
                                   if isfile(path)]:
        m = md5()
        with open(join(dir,filename), 'rb') as file:
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
                with open(join(dir,fn)) as f:
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
        
        with open(join(dir, filename), 'wb') as f:
            f.write(file)
        if not mute:
            print('Saved')
            
        
    if not mute:
        print('Done.')
    if not auto:
        input('Press enter> ')
        
if __name__ == '__main__':
    # Посмотреть, что дано.
    # Если даны токен, мыло и пароль — проверить валидность токена
    # если токен валиден — работать с ним, если нет — попытатьса авторизоваться
    # по мылу и паролю, если не получилось — вывалиться с ошибкой, иначе 
    # работать.
    
    argparser = createParser()
    args = argparser.parse_args()

    if ((not args.email) or (not args.password)) and args.auto:
        raise IOError('have no email and password in auto mode')
    if not args.email:
        args.email = input('email> ')
    if not args.password:
        args.password = getpass('password> ')


    while not isdir(args.dir):
        if isfile(args.dir):
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
            makedirs(args.dir)
            
    main(args.email, args.password, args.dir, args.auto, args.mute)
            
    

    
    
    

