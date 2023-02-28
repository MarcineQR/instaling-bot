import datetime
import json
import time

from utils import *
from selenium import webdriver
from selenium.webdriver.common.by import By


def log_into(login, password):
    browser.get("https://instaling.pl/teacher.php?page=login")

    interact(browser, Dom.SEND_KEYS, By.XPATH, '//*[@id="log_email"]', 1, login)
    interact(browser, Dom.SEND_KEYS, By.XPATH, '//*[@id="log_password"]', 1, password)

    interact(browser, Dom.CLICK, By.XPATH, '/html/body/div/div[3]/form/div/div[3]/button')

    if check_if_element_exist(browser, By.XPATH, '//*[@id="student_panel"]/h4', False):
        interact(browser, Dom.CLICK, By.XPATH, '//*[@id="student_panel"]/p[10]/a')
        return

    interact(browser, Dom.CLICK, By.XPATH, '//*[@id="student_panel"]/p[1]/a')

    time.sleep(0.5)

    interact(browser, Dom.CLICK, By.CSS_SELECTOR, '#continue_session_button')
    interact(browser, Dom.CLICK, By.CSS_SELECTOR, '#start_session_button')

    session()


def session():
    while True:
        if check_if_element_exist(browser, By.CSS_SELECTOR, '#return_mainpage', True):
            interact(browser, Dom.CLICK, By.XPATH, '//*[@id="student_panel"]/p[10]/a')
            break

        interact(browser, Dom.CLICK, By.CSS_SELECTOR, '#know_new')
        interact(browser, Dom.CLICK, By.CSS_SELECTOR, '#skip')
        interact(browser, Dom.CLICK, By.XPATH, '//*[@id="nextword"]')

        if check_if_element_exist(browser, By.XPATH, '#know_new'):
            continue

        time.sleep(0.5)

        word = interact(browser, Dom.INNER_HTML, By.XPATH, '//*[@id="question"]/div[2]/div[2]')
        sentence = interact(browser, Dom.INNER_HTML, By.XPATH, '//*[@id="question"]/div[1]')

        file = open('word.json')
        words = json.load(file)
        file.close()

        for word_json in words:
            if word == word_json['word'] and sentence == word_json['sentence']:
                translation = word_json['translation']
                interact(browser, Dom.SEND_KEYS, By.XPATH, '//*[@id="answer"]', 1, translation)
                words.remove(word_json)
                break

        time.sleep(0.5)

        interact(browser, Dom.CLICK, By.XPATH, '//*[@id="check"]')

        time.sleep(0.5)

        words.append({'word': word, 
                      'sentence': sentence, 
                      'translation': get_translation(sentence.split(" "), 
                                     interact(browser, Dom.INNER_HTML, By.XPATH, '//*[@id="answer_page"]/div[1]/div[1]').split(" "))})

        file = open('word.json', "w")
        json.dump(words, file)
        file.close()

        time.sleep(0.5)


edge_options = webdriver.EdgeOptions()
edge_options.add_argument("--mute-audio")
browser = webdriver.Edge(executable_path='msedgedriver.exe', options=edge_options)

file = open('user.json')
users = json.load(file)
file.close()

date = datetime.datetime.now().strftime("%x")

for user in users:
    if user['last'] == date:
        continue

    log_into(user['login'], user['password'])

    user['last'] = date
    file = open('user.json', "w")
    json.dump(users, file)
    file.close()

browser.quit()
