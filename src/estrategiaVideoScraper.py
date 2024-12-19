from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time




def get_video_links(url, data):

    links = []
    driver = webdriver.Chrome()
    
    try:
        driver.get(url)
        time.sleep(4) 
        
        #login
        login_element = driver.find_element(By.NAME, "loginField")

        login_element.send_keys(data['email'])

        password_element = driver.find_elements(By.NAME, "passwordField")
        password_element[1].send_keys(data['password'])

        time.sleep(.5)
        button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        button.click()

        time.sleep(8)
        
        # here we'll need to iterate for each course
        courses = driver.find_elements(By.CSS_SELECTOR, "a[class='sc-cHGsZl cbCIXA'")

        # for now we'll click the first one
        courses[0].click()
        time.sleep(5)



        # here we'll need to iterate for each class
        lessons = driver.find_elements(By.CSS_SELECTOR, 'div[class="LessonCollapseHeader-title"]')

        # for now we'll click the first one
        lessons[0].click()
        time.sleep(1)

        

        # here we'll need to iterate for each video
        videos_parent = driver.find_element(By.CSS_SELECTOR, 'div[class="StyledScrollbars ListVideos-items"]')
        videos = videos_parent.find_elements(By.XPATH, './*')
        videos = list(map(lambda el: el.find_element(By.XPATH, "./*"),videos))

        print(len(videos))
        c = 1
        driver.execute_script("arguments[0].scrollIntoView(false);", videos_parent)
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(1)

        download_dropdown = driver.find_element(By.CSS_SELECTOR, 'div[class="sc-gPEVay jEUgXm"]')
        download_dropdown.click()

        for video in videos:
            child_width = video.size['width']

            time.sleep(1)

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
                time.sleep(1)
                print(f'video {c} clicked')
            finally:
                time.sleep(.5)
                driver.execute_script("arguments[0].scrollIntoView(false);", videos_parent)
                time.sleep(.5)
                driver.execute_script("window.scrollBy(0, 600);")
                time.sleep(.5)
                driver.execute_script("arguments[0].scrollLeft  = arguments[0].scrollLeft  + arguments[1];", videos_parent, child_width)
                time.sleep(.5)
                downloadButton = driver.find_elements(By.XPATH, "//*[text()='720p']")[1]
                href_value = downloadButton.get_attribute("href")
                links.append(href_value)


            
            c+=1
            time.sleep(1)
            # driver.refresh()
            # time.sleep(5)





    finally:
        driver.quit()