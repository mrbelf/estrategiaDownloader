import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
import time
import os

SELENIUM_LOG_LEVEL = logging.CRITICAL
SELENIUM_HEADLESS = False
START_DRIVER_DELAY = 5
LOGIN_FILL_DELAY = .2
LOGIN_DELAY = 10
COURSE_SELECTION_DELAY = 6
LESSON_SELECTION_DELAY = 6
VIDEO_SELECTION_DELAY = 1.5
SCROLL_DELAY = .2


class DataScrapper:
    def __init__(self, courses_url, user_login, user_password, selenium_logs=False):
        self.courses_url = courses_url
        self.user_login = user_login
        self.user_password = user_password
        self.selenium_logs = selenium_logs
        

    def _start_driver(self, url):
        logging.getLogger('selenium').setLevel(SELENIUM_LOG_LEVEL)
        logging.getLogger('urllib3').setLevel(SELENIUM_LOG_LEVEL)
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(SELENIUM_LOG_LEVEL)

        chrome_options = Options()
        if not self.selenium_logs:
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

        self.driver = driver
        return driver

    def _close_driver(self):
        self.driver.quit()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        self.driver = None

    def _login(self):
        login_element = self.driver.find_element(By.NAME, "loginField")

        login_element.send_keys(self.user_login)

        password_element = self.driver.find_elements(By.NAME, "passwordField")
        password_element[1].send_keys(self.user_password)

        time.sleep(LOGIN_FILL_DELAY)
        button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        button.click()
        
        time.sleep(LOGIN_DELAY)

    # Course
    def _get_course_title(self, course_element):
        return course_element.find_element(By.CSS_SELECTOR, 'h1[class="sc-ksYbfQ fVYfnB"]').text
        

    def _get_courses(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "a[class='sc-cHGsZl cbCIXA'")

    def _total_courses(self):
        return len(self._get_courses())

    def _get_course_index(self, name):
        for index,course in enumerate(self._get_courses()):
            if self._get_course_title(course) == name:
                return index
        print(f'Course of name {name} not found')

    def _get_course(self, index):
        return self._get_courses()[index]

    def _enter_course(self, courseName):
        index = self._get_course_index(courseName)
        course = self._get_course(index)

        self.driver.execute_script("arguments[0].scrollIntoView(false);", course)
        time.sleep(SCROLL_DELAY)
        self.driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(SCROLL_DELAY)

        course.click()
        time.sleep(COURSE_SELECTION_DELAY)
    #end Course

    #Lessons
    def _get_lesson_title(self, lesson_element):
        return lesson_element.find_element(By.XPATH, './*').text

    def _get_lessons(self):
        return self.driver.find_elements(By.CSS_SELECTOR, 'div[class="LessonCollapseHeader-title"]')

    def _get_lesson(self, index):
        return self._get_lessons()[index]

    def _get_lesson_index(self, name):
        for index,lesson in enumerate(self._get_lessons()):
            if self._get_lesson_title(lesson) == name:
                return index
        print(f'Lesson of name {name} not found')

    def _get_lesson_titles(self):
        return list(map(lambda lesson: self._get_lesson_title(lesson),self._get_lessons()))

    def _open_lesson(self, lesson_name):
        lesson = self._get_lesson(self._get_lesson_index(lesson_name))

        self.driver.execute_script("arguments[0].scrollIntoView(false);", lesson)
        time.sleep(SCROLL_DELAY)
        self.driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(SCROLL_DELAY)
        lesson.click()
        print(f'{lesson_name} clicked')
        time.sleep(LESSON_SELECTION_DELAY)

    def _get_pdf_from_open_lesson(self):
        pdf_buttons_parent = self.driver.find_element(By.CSS_SELECTOR, 'div[class="LessonButtonList"]')
        pdf_buttons = pdf_buttons_parent.find_elements(By.XPATH, "./*")
        
        original_pdf_button = None
        for button in pdf_buttons:
            element_with_text = button.find_elements(By.XPATH, ".//*[contains(text(),'versão original')]")
            if element_with_text:
                original_pdf_button = button

        if original_pdf_button:
            return original_pdf_button.get_attribute("href")
        print('Could not find pdf')
        

    #end Lessons

    def _get_videos_for_open_class(self):
        links = []
        videos_parent = self.driver.find_element(By.CSS_SELECTOR, 'div[class="StyledScrollbars ListVideos-items"]')
        videos = videos_parent.find_elements(By.XPATH, './*')
        videos = list(map(lambda el: el.find_element(By.XPATH, "./*"),videos))

        self.driver.execute_script("arguments[0].scrollIntoView(false);", videos_parent)
        time.sleep(SCROLL_DELAY)
        self.driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(SCROLL_DELAY)

        c = 1
        download_dropdown = self.driver.find_element(By.CSS_SELECTOR, 'div[class="sc-gPEVay jEUgXm"]')
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
                self.driver.execute_script("arguments[0].scrollIntoView(false);", videos_parent)
                time.sleep(SCROLL_DELAY)
                self.driver.execute_script("window.scrollBy(0, 600);")
                time.sleep(SCROLL_DELAY)
                self.driver.execute_script("arguments[0].scrollLeft  = arguments[0].scrollLeft  + arguments[1];", videos_parent, child_width)
                time.sleep(SCROLL_DELAY)
                downloadButton = self.driver.find_elements(By.XPATH, "//*[text()='720p']")[1]
                link = downloadButton.get_attribute("href")
                links.append((title, link))

            c+=1
        return links


    #=============== For External usage ===============#
    def get_all_courses(self):
        self._start_driver(self.courses_url)
        try:
            self._login()

            courses = self._get_courses()

            course_titles = list(map(lambda el: self._get_course_title(el),courses))
        finally:
            self._close_driver()
        return course_titles

    def get_all_lessons(self, course):
        self._start_driver(self.courses_url)
        try:
            self._login()
            self._enter_course(course)

            lessons = self._get_lesson_titles()
        finally:
            self._close_driver()
        return lessons

    def get_video_links(self, course, lesson):
        self._start_driver(self.courses_url)
        
        try:
            self._login()
            self._enter_course(course)

            self._open_lesson(lesson)
            links = self._get_videos_for_open_class()
        finally:
            self._close_driver()

        return links

    def get_pdf_link(self, course, lesson):
        self._start_driver(self.courses_url)

        try:
            self._login()
            self._enter_course(course)
            self._open_lesson(lesson)
            return self._get_pdf_from_open_lesson()
            
        finally:
            self._close_driver()
