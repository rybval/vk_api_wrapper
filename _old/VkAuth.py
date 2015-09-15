import requests
from selenium import webdriver

def vkauth(user, password):
    driver = webdriver.Firefox()

    driver.get("http://api.vkontakte.ru/oauth/authorize?"
               "client_id=4805647&scope=friends,photos,audio,video,docs,notes,pages,status,wall,groups,messages,email,notifications,stats,ads" #offline"
               "&redirect_uri=http://api.vk.com/blank.html"
               "&display=page&response_type=token")

    user_input = driver.find_element_by_name("email")
    user_input.send_keys(user)
    password_input = driver.find_element_by_name("pass")
    password_input.send_keys(password)

    submit = driver.find_element_by_id("install_allow")

    submit.click()

    current = driver.current_url
    access_list = (current.split("#"))[1].split("&")
    driver.close()

    return {"access_token":(access_list[0].split("="))[1] , "expires_in":(access_list[1].split("="))[1], "user_id":(access_list[2].split("="))[1]}
    
if __name__ == "__main__":
    d = vkauth()
    print (d)
    input()
