# from selenium import webdriver
# import time
# import psycopg2
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# import os
#
# driver = webdriver.Chrome(executable_path='C://Users/Deniss/PycharmProjects/two_factor_auth/sweater/chromedriver.exe')
# driver.get('http://127.0.0.1:5000/register')
# time.sleep(1)
# connection = psycopg2.connect(os.environ['TEST_DATABASE_URL'])
# connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# cursor = connection.cursor()
# query = """
#             SELECT login,password, FROM users WHERE login='login1'
# """
#
#
# def test_current_registration():
#     driver.find_element_by_id('login').send_keys('login1')
#     driver.find_element_by_id('password').send_keys('password')
#     driver.find_element_by_id('repeat_password').send_keys('password')
#     for i in range(1, 6):
#         driver.find_element_by_id(i).click()
#         time.sleep(1)
#     driver.find_element_by_id('registerButton').click()
#     cursor.execute(query)
#     print(cursor.fetchall())
#
#
# test_current_registration()
# driver.close()

from selenium.webdriver.support.ui import Select
from selenium import webdriver
import time
import math
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import pytest
from selenium import webdriver
import math



@pytest.fixture(scope="function")
def browser():
    print("\nstart browser for test..")
    browser = webdriver.Chrome(executable_path='C://Users/Deniss/PycharmProjects/two_factor_auth/sweater/chromedriver.exe')
    yield browser
    print("\nquit browser..")
    browser.quit()

# @pytest.mark.parametrize('counter', range(1,8))
def test_guest_should_see_login_link(browser, counter=1):
    num = 236894
    answer = math.log(int(time.time()))
    link = f"https://stepik.org/lesson/{num+counter}/step/1"
    browser.get(link)

    browser.implicitly_wait(10)

    print(counter)
    time.sleep(10)
    browser.find_element_by_tag_name('textarea').send_keys(answer)
    print(counter+1)
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.TAG_NAME, "button")))
    browser.find_element_by_tag_name('button').click()
    time.sleep(10)

