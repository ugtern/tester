from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.get("http://operator.webchat.newcontact.su/")

time.sleep(2)
driver.find_element_by_id('login').send_keys('oper')
time.sleep(1)
driver.find_element_by_id('password').send_keys('oper')
time.sleep(1)
driver.find_element_by_id('submit-button').click()