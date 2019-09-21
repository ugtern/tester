from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.get("http://test.webchat.newcontact.su/")

time.sleep(2)
driver.find_element_by_id('take_user_name').send_keys('test')
time.sleep(1)
driver.find_element_by_id('take_user_name_close').click()
time.sleep(1)
driver.find_element_by_id('web-chat_new-message').send_keys('test')
time.sleep(1)
driver.find_element_by_id('web-chat_submit-message').click()
