import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
import time
import os

LOGS_ENABLED = False
SELENIUM_LOG_LEVEL = logging.CRITICAL
SELENIUM_HEADLESS = False
START_DRIVER_DELAY = 5
LOGIN_FILL_DELAY = .2
LOGIN_DELAY = 10
COURSE_SELECTION_DELAY = 6
LESSON_SELECTION_DELAY = 6
VIDEO_SELECTION_DELAY = 1.5
SCROLL_DELAY = .2


def start_driver(url):
    logging.getLogger('selenium').setLevel(SELENIUM_LOG_LEVEL)
    logging.getLogger('urllib3').setLevel(SELENIUM_LOG_LEVEL)
    logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(SELENIUM_LOG_LEVEL)

    chrome_options = Options()
    if not LOGS_ENABLED:
        sys.stdout = sys.stderr = open(os.devnull, 'w')

        logging.getLogger('tensorflow').setLevel(logging.ERROR)
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--silent")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    if SELENIUM_HEADLESS:
        chrome_options.add_argument("--headless")


    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(START_DRIVER_DELAY)
    return driver

def close_driver(driver):
    driver.quit()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

def login(driver, data):
    login_element = driver.find_element(By.NAME, "loginField")

    login_element.send_keys(data['email'])

    password_element = driver.find_elements(By.NAME, "passwordField")
    password_element[1].send_keys(data['password'])

    time.sleep(LOGIN_FILL_DELAY)
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    button.click()
    
    time.sleep(LOGIN_DELAY)

# Course
def get_course_title(course_element):
    return course_element.find_element(By.CSS_SELECTOR, 'h1[class="sc-ksYbfQ fVYfnB"]').text
    

def get_courses(driver):
    return driver.find_elements(By.CSS_SELECTOR, "a[class='sc-cHGsZl cbCIXA'")

def total_courses(driver):
    return len(get_courses(driver))

def get_course_index(driver, name):
    for index,course in enumerate(get_courses(driver)):
        if get_course_title(course) == name:
            return index
    print(f'Course of name {name} not found')

def get_course(driver, index):
    return get_courses(driver)[index]

def enter_course(driver, courseName):
    index = get_course_index(driver ,courseName)
    course = get_course(driver,index)

    driver.execute_script("arguments[0].scrollIntoView(false);", course)
    time.sleep(SCROLL_DELAY)
    driver.execute_script("window.scrollBy(0, 200);")
    time.sleep(SCROLL_DELAY)

    course.click()
    time.sleep(COURSE_SELECTION_DELAY)
#end Course

#Lessons
def get_lesson_title(lesson_element):
    return lesson_element.find_element(By.XPATH, './*').text

def get_lessons(driver):
    return driver.find_elements(By.CSS_SELECTOR, 'div[class="LessonCollapseHeader-title"]')

def get_lesson(driver, index):
    return get_lessons(driver)[index]

def get_lesson_index(driver, name):
    for index,lesson in enumerate(get_lessons(driver)):
        if get_lesson_title(lesson) == name:
            return index
    print(f'Lesson of name {name} not found')

def get_lesson_titles(driver):
    return list(map(lambda lesson: get_lesson_title(lesson),get_lessons(driver)))

def open_lesson(driver, lesson_name):
    lesson = get_lesson(driver, get_lesson_index(driver, lesson_name))

    driver.execute_script("arguments[0].scrollIntoView(false);", lesson)
    time.sleep(SCROLL_DELAY)
    driver.execute_script("window.scrollBy(0, 200);")
    time.sleep(SCROLL_DELAY)
    lesson.click()
    print(f'{lesson_name} clicked')
    time.sleep(LESSON_SELECTION_DELAY)
#end Lessons

def get_videos_for_open_class(driver):
    links = []
    videos_parent = driver.find_element(By.CSS_SELECTOR, 'div[class="StyledScrollbars ListVideos-items"]')
    videos = videos_parent.find_elements(By.XPATH, './*')
    videos = list(map(lambda el: el.find_element(By.XPATH, "./*"),videos))

    driver.execute_script("arguments[0].scrollIntoView(false);", videos_parent)
    time.sleep(SCROLL_DELAY)
    driver.execute_script("window.scrollBy(0, 600);")
    time.sleep(SCROLL_DELAY)

    c = 1
    download_dropdown = driver.find_element(By.CSS_SELECTOR, 'div[class="sc-gPEVay jEUgXm"]')
    download_dropdown.click()

    for video in videos:
        child_width = video.size['width']
        title = video.find_element(By.CSS_SELECTOR, 'span[class="VideoItem-info-title"]').text

        try:
            video.click()
        except:
            print(f'fail on clicking video {c}')
            print(f'second attempt to click video {c}')
            try:
                video.click()
            except Exception as e:
                print(f'second fail to click video {c}')
                #raise e
        else:
            time.sleep(VIDEO_SELECTION_DELAY)
            print(f'video {c} clicked')
        finally:
            driver.execute_script("arguments[0].scrollIntoView(false);", videos_parent)
            time.sleep(SCROLL_DELAY)
            driver.execute_script("window.scrollBy(0, 600);")
            time.sleep(SCROLL_DELAY)
            driver.execute_script("arguments[0].scrollLeft  = arguments[0].scrollLeft  + arguments[1];", videos_parent, child_width)
            time.sleep(SCROLL_DELAY)
            downloadButton = driver.find_elements(By.XPATH, "//*[text()='720p']")[1]
            link = downloadButton.get_attribute("href")
            links.append((title, link))

        c+=1
    return links


#=============== For External usage ===============#
def get_all_courses(url, data):
    driver = start_driver(url)
    try:
        login(driver, data)

        courses = get_courses(driver)

        course_titles = list(map(lambda el: get_course_title(el),courses))
    finally:
        close_driver(driver)
    return course_titles

def get_all_lessons(url, data, course):
    driver = start_driver(url)
    try:
        login(driver, data)
        enter_course(driver, course)

        lessons = get_lesson_titles(driver)
    finally:
        close_driver(driver)
    return lessons

def get_video_links(url, data, course, lesson):
    driver = start_driver(url)
    
    try:
        login(driver, data)
        
        enter_course(driver, course)

        open_lesson(driver, lesson)
        
        links = get_videos_for_open_class(driver)
    finally:
        close_driver(driver)

    return links
