import os
import requests
from selenium import webdriver
import json

driver = webdriver.Firefox()

driver.get("http://api.vkontakte.ru/oauth/authorize?"
           "client_id=4805647&scope=audio"
           "&redirect_uri=http://api.vk.com/blank.html"
           "&display=page&response_type=token")

user = "yoroshiku"
password = "Kae[ilei2bohfohgilie"

user_input = driver.find_element_by_name("email")
user_input.send_keys(user)
password_input = driver.find_element_by_name("pass")
password_input.send_keys(password)

submit = driver.find_element_by_id("install_allow")

submit.click()
print('Clicked')

current = driver.current_url
access_list = (current.split("#"))[1].split("&")
access_token = (access_list[0].split("="))[1] # acces_token
expires_in = (access_list[1].split("="))[1]
user_id = (access_list[2].split("="))[1] 
driver.close()

print (access_token+" "+expires_in+" "+user_id)

print "Connecting"

url = "https://api.vkontakte.ru/method/" \
      "audio.get?uid=" + user_id +\
      "&access_token=" + access_token

artists_list = []
titles_list = []
links_list = []

number = 0

page = requests.get(url)
html = page.text

my_dict = json.loads(html) #

for i in my_dict['response']:
    artists_list.append(i['artist'])
    titles_list.append(i['title'])
    links_list.append(i['url'])
    number += 1



path = "downloads"

if not os.path.exists(path):
    os.makedirs(path)

print "Need to download: ", number



for i in range(0, number):
    artists_list[i] = (artists_list[i].replace('/','_')).replace('\\','_').replace('?','_').replace('*','_').replace(':','_').replace('"','_').replace('|','_').replace('<','_').replace('>','_')
    titles_list[i] = (titles_list[i].replace('/','_')).replace('\\','_').replace('?','_').replace('*','_').replace(':','_').replace('"','_').replace('|','_').replace('<','_').replace('>','_')
    new_filename = path+"/"+artists_list[i] + " - " + titles_list[i] + ".mp3"
    if len(new_filename) > 200:
        new_filename = new_filename[:200] + ".mp3"
        
    print "Downloading: ", new_filename, i

    if not os.path.exists(new_filename):

        with open(new_filename, "wb") as out:
            response = requests.get(links_list[i].split("?")[0])
            out.write(response.content)

print "Download complete."

input()

