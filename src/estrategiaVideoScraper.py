from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time




def get_video_links(url, data):

    driver = webdriver.Chrome()
    
    try:
        driver.get(url)
        time.sleep(5) 
        
        login_element = driver.find_element(By.NAME, "loginField")

        login_element.send_keys(data['email'])

        password_element = driver.find_elements(By.NAME, "passwordField")
        password_element[1].send_keys(data['password'])

        time.sleep(1)
        button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        button.click()

        time.sleep(10)
        
        # here we'll need to iterate for each course
        courses = driver.find_elements(By.CSS_SELECTOR, "a[class='sc-cHGsZl cbCIXA'")
        print(len(courses))

        # for now we'll click the first one
        courses[0].click()

        time.sleep(10)

    finally:
        driver.quit()