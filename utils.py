from enum import Enum

from selenium.webdriver.support.ui import WebDriverWait


class Dom(Enum):
    SEND_KEYS = 0
    CLICK = 1
    INNER_HTML = 2


def interact(browser, operation, by, path, time=1.0, keys=None):
    element = wait(browser, by, path, time)
    try:
        match operation:
            case Dom.SEND_KEYS:
                element.send_keys(keys)
            case Dom.CLICK:
                element.click()
            case Dom.INNER_HTML:
                return element.get_attribute('innerHTML')
    except:
        pass


def wait(browser, by, path, time):
    try:
        return WebDriverWait(browser, timeout=time).until(lambda d: d.find_element(by, path))
    except:
        pass


def check_if_element_exist(browser, by, xpath, click = False):
    try:
        element = browser.find_element(by, xpath)
        if click:
            element.click()
    except:
        return False
    else:
        return True
    

def get_translation(before, after):
    if len(before) != len(after):
        return ''

    translation = str()
    signs = [".", ",", "?", "!", ":", ";", "\'s", "\'", "\""]
    
    for index in range(len(before)):
        if '_' in before[index]:
            if len(translation) > 0:
                translation += ' '
            translation += after[index]

    for sign in signs:
        translation = translation.replace(sign,'')
    return translation

