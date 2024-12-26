from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


LOGIN_DELAY = 8
COURSE_SELECTION_DELAY = 5
LESSON_SELECTION_DELAY = 1
VIDEO_SELECTION_DELAY = 1
SCROLL_DELAY = .5


def start_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def login(driver, data):
    login_element = driver.find_element(By.NAME, "loginField")

    login_element.send_keys(data['email'])

    password_element = driver.find_elements(By.NAME, "passwordField")
    password_element[1].send_keys(data['password'])

    time.sleep(.5)
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    button.click()

def get_courses(driver):
    return driver.find_elements(By.CSS_SELECTOR, "a[class='sc-cHGsZl cbCIXA'")

def total_courses(driver):
    return len(get_courses(driver))

def get_course(driver, index):
    return get_courses(driver)[index]

def enter_course(driver, index):
    get_course(driver,index).click()

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
            href_value = downloadButton.get_attribute("href")
            links.append(href_value)
            time.sleep(.1)

        c+=1
        time.sleep(1)
    return links

def get_video_links(url, data):
    driver = start_driver(url)
    
    try:
        time.sleep(4) 
        
        #login
        login(driver, data)
        time.sleep(LOGIN_DELAY)

        
        # here we'll need to iterate for each course
        enter_course(driver,0)
        time.sleep(COURSE_SELECTION_DELAY)

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