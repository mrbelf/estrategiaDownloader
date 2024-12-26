from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

START_DRIVER_DELAY = 4
LOGIN_FILL_DELAY = .5
LOGIN_DELAY = 8
COURSE_SELECTION_DELAY = 5
LESSON_SELECTION_DELAY = 1
VIDEO_SELECTION_DELAY = 1
SCROLL_DELAY = .5


def start_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(START_DRIVER_DELAY)
    return driver

def login(driver, data):
    login_element = driver.find_element(By.NAME, "loginField")

    login_element.send_keys(data['email'])

    password_element = driver.find_elements(By.NAME, "passwordField")
    password_element[1].send_keys(data['password'])

    time.sleep(LOGIN_FILL_DELAY)
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    button.click()
    
    time.sleep(LOGIN_DELAY)

def get_courses(driver):
    return driver.find_elements(By.CSS_SELECTOR, "a[class='sc-cHGsZl cbCIXA'")

def total_courses(driver):
    return len(get_courses(driver))

def get_course(driver, index):
    return get_courses(driver)[index]

def enter_course(driver, index):
    get_course(driver,index).click()
    time.sleep(COURSE_SELECTION_DELAY)

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
        course_titles = list(map(lambda el: el.find_element(By.CSS_SELECTOR, 'h1[class="sc-ksYbfQ fVYfnB"]').text,courses))
    finally:
        driver.quit()
    return course_titles

def get_video_links(url, data):
    driver = start_driver(url)
    
    try:
        login(driver, data)
        
        # here we'll need to iterate for each course
        enter_course(driver,0)

        # here we'll need to iterate for each class
        lessons = driver.find_elements(By.CSS_SELECTOR, 'div[class="LessonCollapseHeader-title"]')

        # for now we'll click the first one
        lessons[0].click() 
        time.sleep(LESSON_SELECTION_DELAY)

        

        # here we'll need to iterate for each video
        links = get_videos_for_open_class(driver)
        
        print(links)

    finally:
        driver.quit()