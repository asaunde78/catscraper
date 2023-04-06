
from selenium import webdriver
# help(selenium)
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options


# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager

from bs4 import BeautifulSoup

import urllib.parse 
import time

import traceback

class catscraper():
    def __init__(self,offset=0,jump=1):
        self.offset = offset
        self.jump = jump
        options = Options()
        
        # options.binary_location = "/home/asher/catscraper/webdriver/chromedriver"
        options.add_argument('lang=en') 
        options.add_argument('--headless') 
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')


        # driver = ChromeDriverManager(path="driver").install()
        # driver = ChromeDriverManager(path="driver",chrome_type=ChromeType.CHROMIUM).install()
        # driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        driver = GeckoDriverManager(path="driver").install()

        #print(driver)
        # self.driver = webdriver.Chrome(driver,options=options)
        self.driver = webdriver.Firefox(driver,options=options)


        self.max_missed = 30
        #self.driver.get("https://www.google.com/search")
    
    def find_image_urls(self, search, num):
        start = time.time()
        url = "https://www.google.com/search"
        #headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"}
        #search = "cat"
        params = {
            "q":search,
            "tbm": "isch",                # image results
            "hl": "en",                   # language of the search
            "gl": "us",                   # country where search comes from
            "ijn": "0"                    # page number
        }

        query_string = urllib.parse.urlencode(params)

        
        print(self.driver.title)

        print("[INFO] Gathering image links")
        image_urls=[]
        count = 0
        missed_count = 0
        self.driver.get(f"{url}?{query_string}")
        time.sleep(3)
        indx = 1
        while num > count:
            begin = time.time()
            try:
                #find and click image
                

                imgurl = self.driver.find_element(By.XPATH,'//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'%(str(self.offset + self.jump*indx)))
                imgurl.click()
                time.sleep(3)
                missed_count = 0
            except Exception:
                print("missed")
                missed_count = missed_count + 1
                if (missed_count>self.max_missed):
                    print("[INFO] Maximum missed photos reached, exiting...")
                    break

            try:
                #select image from the popup
                #time.sleep(1)
                class_names = ["n3VNCb"]
                
                images = [self.driver.find_elements(By.CLASS_NAME, class_name) for class_name in class_names if len(self.driver.find_elements(By.CLASS_NAME, class_name)) != 0 ][0]
                
                for i_,image in enumerate(images):
                    # begin = time.time()
                    # ending = time.time()
                    # print(f"finding elements took {ending-begin}")
                    #only download images that starts with http
                    src_link = image.get_attribute("src")
                    # print(i_)
                    if(("http" in  src_link) and (not "encrypted" in src_link)):
                        print(
                            f"[INFO] {search} \t #{count} \t {src_link}")
                        image_urls.append(src_link)
                        count +=1
                        ending = time.time()
                        print(f"clicking took {ending-begin}")
                        break
            except Exception as e:
                print("[INFO] Unable to get link: ", e)
                print(traceback.format_exc())

            try:
                #scroll page to load next image
                if(count%3==0):
                    self.driver.execute_script("window.scrollTo(0, "+str(indx*60)+");")
                element = self.driver.find_element(By.CLASS_NAME,"mye4qd")
                element.click()
                print("[INFO] Loading next page")
                time.sleep(3)
            except Exception:
                time.sleep(1)
            indx += 1


        # self.driver.quit()
        print("[INFO] Google search ended")
        end = time.time()
        print(f"Took {end - start} seconds")
        # self.driver.quit()
        return image_urls
    



