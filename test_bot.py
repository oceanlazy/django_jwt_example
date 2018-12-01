import uuid
import random

import requests
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys

import test_bot_settings


def browser_signup(username, password, email):
    driver.get("http://127.0.0.1:8000/accounts/signup/")
    driver.find_element_by_id("id_username").send_keys(username)
    driver.find_element_by_id("id_email").send_keys(email)
    driver.find_element_by_id("id_password1").send_keys(password)
    driver.find_element_by_id("id_password2").send_keys(password + Keys.RETURN)
    return username, password


def browser_login(username, password):
    driver.get("http://127.0.0.1:8000/accounts/login/")
    driver.find_element_by_id("id_username").send_keys(username)
    driver.find_element_by_id("id_password").send_keys(password + Keys.RETURN)


def browser_post_make():
    driver.get("http://127.0.0.1:8000/posts/")
    for i in range(int(test_bot_settings.max_posts_per_user/2)):
        driver.find_element_by_id("id_title").send_keys(str((uuid.uuid4())))
        driver.find_element_by_id("id_text").send_keys(str((uuid.uuid4())))
        driver.find_element_by_id("id_slug").send_keys(str((uuid.uuid4())) + Keys.RETURN)


def browser_post_like():
    driver.get("http://127.0.0.1:8000/posts/")
    likes = driver.find_elements_by_id("like")
    unlikes = driver.find_elements_by_id("unlike")
    for i in range(int(test_bot_settings.max_likes_per_user/2)):
        try:
            if random.randint(0, 1):
                likes[random.randint(0, len(likes) - 1)].click()  # click like button on random post
            else:
                unlikes[random.randint(0, len(unlikes) - 1)].click()  # click like button on random post
        except exceptions.StaleElementReferenceException:
            pass


users = [(str((uuid.uuid4())), 'testpass_313', 'exmaple@mail.com') for _ in range(test_bot_settings.number_of_users)]
driver = webdriver.Chrome()
for username, password, email in users[:int(len(users) / 2)]:
    browser_signup(username, password, email)
    browser_post_make()
    browser_post_like()
    driver.get('http://127.0.0.1:8000/accounts/logout/')

driver.close()

for username, password, email in users[int(len(users) / 2):]:
    # create user
    response = requests.post("http://localhost:8000/api/users/", data={'username': username,
                                                                       'password': 'testpass_313',
                                                                       'email': 'exmaple@mail.com'})
    print(response.text)
    # get token
    response = requests.post('http://127.0.0.1:8000/api/token/obtain/', data={'username': username,
                                                                              'password': 'testpass_313'})
    access_token = response.json()['access']
    # make post
    articles_titles = [str(uuid.uuid4())[:20] for _ in range(int(test_bot_settings.max_posts_per_user / 2))]
    for title in articles_titles:
        response = requests.post('http://127.0.0.1:8000/api/posts/', data={'title': title,
                                                                           'text': str((uuid.uuid4()))},
                                 headers={'Authorization': 'Bearer {}'.format(access_token)})
        print(response.text)
    # like post
    for i in range(int(test_bot_settings.max_likes_per_user/2)):
        slug = articles_titles[random.randint(0, len(articles_titles) - 1)]  # find some random article slug
        if random.randint(0, 1):
            response = requests.post('http://127.0.0.1:8000/api/posts/{}/'.format(slug),
                                     headers={'Authorization': 'Bearer {}'.format(access_token)})
        else:
            response = requests.delete('http://127.0.0.1:8000/api/posts/{}/'.format(slug),
                                       headers={'Authorization': 'Bearer {}'.format(access_token)})
        print(response.text)
