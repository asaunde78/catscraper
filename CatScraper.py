
from selenium import webdriver
# help(selenium)
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options


from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.utils import ChromeType
# from webdriver_manager.firefox import GeckoDriverManager


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver import ActionChains


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
        
        # options.add_argument('--start-maximized') 
        # options.headless = True
        options.add_argument('--headless=new') 
        # options.add_argument('--single-process')

        options.add_argument('--no-sandbox')
        options.page_load_strategy = 'none'
        
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--disable-extensions')
        options.add_extension("blockerextension.crx")

        options.add_argument('--disable-infobars')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        try:
            self.driver = webdriver.Chrome("/usr/bin/chromedriver",options=options)
        except Exception: 
            driver = ChromeDriverManager(path="driver").install()
            self.driver = webdriver.Chrome(driver,options=options)
        # self.driver = webdriver.Firefox(driver,options=options)

        # self.actions = ActionChains(self.driver)
        self.tries = 1
        self.driver.get("https://www.google.com")
        
        # self.driver.get("https://www.google.com/search")
        #time.sleep(2)
    def quit(self):
        self.driver.quit()
    def generateXPATH(self,childElement,current):
        childTag = childElement.tag_name
        if(childTag == "html"):
            return "/html[1]"+current
        parentElement = childElement.find_element(By.XPATH,"..")
        childrenElements = parentElement.find_elements(By.XPATH,"*")
        c = 0
        for cElement in childrenElements:
            cElementTag=cElement.tag_name
            if(childTag == cElementTag):
                c += 1
            if(childElement == cElement):
                return self.generateXPATH(parentElement, "/"+childTag + "[" + str(c) + "]" + current)
        return None

    def getimages(self,search,num):
        self.driver.add_cookie({"name":"count","value":str(num)})
        # c = self.driver.get_cookie("count")["value"]
        # print(f"[COOKIE VALUE] {c}")
        
        time.sleep((0.1 * (self.offset)))
        url = "https://www.google.com/search"
        #headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"}
        #search = "cat"
        params = {
            "q":search,
            "tbm": "isch",                # image results
            "hl": "en",                   # language of the search
            "gl": "us",                   # country where search comes from
            "ijn": "0",                    # page number
            "tbs":"isz:l"
        }

        query_string = urllib.parse.urlencode(params)

        print("[INFO] Gathering image links")
        image_urls=[]
        address = f"{url}?{query_string}"
        
        self.driver.get(address)
        print(f"[{self.offset}] got {address} found {self.driver.title}")
        # time.sleep(3)
        # time.sleep(3)
        # self.driver.execute_script(f"document.documentElement.appendChild(Object.assign(document.createElement(\"div\"),{{className: desired_count, id:{num}}} ));")

        try:
            wait = WebDriverWait(self.driver, 6)
            # wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME,"bRMDJf")))
        except:
            print("didn't work")
            return []
    
        # highest_index = self.offset*self.jump
        highest_index = self.offset#
        count = 0
        while count < num:
            
            thumbnails = self.driver.find_elements(By.CLASS_NAME,"bRMDJf")
            thumbnails = thumbnails[highest_index:][::self.jump]
            # thumbnails = thumbnails[highest_index:][::]
            for nail in thumbnails:

                tries = 0
                while tries < self.tries:
                    try:
                        # print("about to click! so excited")
                        nail.click()
                        # time.sleep(3)
                        image_urls.append("balls")
                        # time.sleep(3)
                        
                        break
                    except Exception as e:
                        print("[ERROR] failed to click: ", e)
                        tries +=1
                        if tries == self.tries:
                            print("[ERROR] RAN OUT OF TRIES :/")
                            return image_urls
                class_name = "f2By0e"
                waitstart = time.time()
                wait = WebDriverWait(self.driver, 15)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name))) # looking for image holder
                count += 1
                print(f"[IMAGE] {self.offset} got image {count}/{num}")
                waitend = time.time()
                print(f"\t [WAIT] {self.offset} Waited {waitend-waitstart} seconds")
                
                if (count== num):
                    wait = WebDriverWait(self.driver, 9999)
                    wait.until(EC.presence_of_element_located((By.ID, f"DONE")))
                    return image_urls
                # wait = WebDriverWait(self.driver, 7)
                # wait.until(EC.presence_of_element_located((By.ID, f"link_count{count}")))
                # print(self.driver.find_element(By.ID, f"link_count{self.count}"))
                highest_index += self.jump#*ind
        # wait = WebDriverWait(self.driver, 7)
        # wait.until(EC.presence_of_element_located((By.ID, f"link_countdone")))
        return image_urls

    
if __name__ == "__main__":
    # c = catscraper(offset=1,jump=2)
    c = catscraper(offset=0,jump=1)
    b = time.time()
    images = c.getimages("owen wilson",10)
    print(images)
    e = time.time()
    print(f"Took {e-b} seconds to generate {len(images)} images")
    c.quit()



