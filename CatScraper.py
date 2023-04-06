
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

from selenium.webdriver import ActionChains


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
        
        options.add_argument('--start-maximized') 
        options.add_argument('--headless') 
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')

        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-gpu')


        # driver = ChromeDriverManager(path="driver").install()
        # driver = ChromeDriverManager(path="driver",chrome_type=ChromeType.CHROMIUM).install()
        # driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        # driver = GeckoDriverManager(path="driver").install()

        #print(driver)
        try:
            self.driver = webdriver.Chrome("/usr/bin/chromedriver",options=options)
        except Exception: 
            driver = ChromeDriverManager(path="driver").install()
            self.driver = webdriver.Chrome(driver,options=options)
        # self.driver = webdriver.Firefox(driver,options=options)

        self.actions = ActionChains(self.driver)
        self.tries = 1
        self.driver.get("https://www.google.com/search")
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
        start = time.time()
        # time.sleep((1 * (self.offset)))
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

        print("[INFO] Gathering image links")
        image_urls=[]
        
        self.driver.get(f"{url}?{query_string}")
        print(self.driver.title)
        # time.sleep(3)
        wait = WebDriverWait(self.driver, 2)
        # wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,"bRMDJf")))
    
        highest_index = self.offset*self.jump

        while len(image_urls) < num:
            
            thumbnails = self.driver.find_elements(By.CLASS_NAME,"bRMDJf")
        
            # l = list(range(len(thumbnails)))
            # print(f"{self.offset} looking at indexes {l[highest_index:][::self.jump]}")
            thumbnails = thumbnails[highest_index:][::]
            if(len(thumbnails) > 0):
                print(f"[LENGTH] Thumbnails length for {self.offset}: ", len(thumbnails))
                print(f"{self.offset} starting at {highest_index}")
                print(f"{self.offset} has {len(thumbnails)} to look at")

            for nail in thumbnails:
                name = nail.find_element(By.CLASS_NAME,"rg_i").get_attribute("alt")
                
                nailxpath =  self.generateXPATH(nail, "")
                print("xpath",nailxpath)
                # print(f'{self.offset} found {name}')
                # print(f"{self.offset}'s element's path: {name}",nailxpath)
                
                tries = 0
                tried_focusing = False
                while tries < self.tries:
                    try:
                
                        # print(f"{self.offset}'s element's img alt: {name}", nail.is_displayed())
                        # print(f"{self.offset}'s element's img alt: {name}", nail.is_enabled())
                        # wait = WebDriverWait(self.driver, 3)
                        # wait.until(EC.element_to_be_clickable((By.XPATH,nailxpath)))
                        # self.driver.implicitly_wait(0.5)
                        # time.sleep(3)
                        nail.click()
                        # thumb = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, nailxpath)))
                        # thumb.click()
                        # self.actions.move_to_element(nail).click().perform()

                        # self.driver.execute_script("document.evaluate(arguments[0],document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,null).singleNodeValue.click()",nailxpath)

                        # self.driver.execute_script("document.querySelector(arguments[0]).click();", nail.)
                        class_name = "n3VNCb"
                        wait = WebDriverWait(self.driver, 3)
                        wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
                        break
                    except Exception as e:
                        # if (not tried_focusing):
                        #     nailxpath =  self.generateXPATH(nail, "")
                        #     self.driver.execute_script("document.evaluate(arguments[0],document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,null).singleNodeValue.focus()",nailxpath)
                        #     tried_focusing = True
                        #     print(f"[{self.offset}FOCUS] Tried focusing" )
                        #     break
                        # nailxpath =  self.generateXPATH(nail, "")
                        # thumb = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, nailxpath)))
                        # thumb.click()
                        # print(f"[{self.offset}FAILED] \n\t name: {name} \n\t path: {nailxpath} ")
                        # self.driver.execute_script("document.evaluate(arguments[0],document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,null).singleNodeValue.click()",nailxpath)
                        print("[ERROR] failed to click: ", e)
                        tries +=1
                        if tries == self.tries:
                            print("[ERROR] RAN OUT OF TRIES :/")
                            return image_urls
                            
                images = self.driver.find_elements(By.CLASS_NAME, class_name)
                for image in images:
                    src_link = image.get_attribute("src")
                    # print(src_link)
                    # if(not("http" in  src_link) or not(not "encrypted" in src_link)):
                    #     print("BAD IMAGE WTF")
                    if(("http" in  src_link) and (not "encrypted" in src_link)):
                        print(
                            f"\t[{self.offset}LINK] \t {src_link}")
                        image_urls.append(src_link)
                        if len(image_urls) >= num:
                            return image_urls
                highest_index += 1#self.jump#*ind
                print(f"new highest index for {self.offset} is {highest_index}")
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"{self.offset} is scrolling")
            # self.driver.implicitly_wait(3)
        # print("reached end :/")
        return image_urls

    
if __name__ == "__main__":
    # c = catscraper(offset=1,jump=2)
    c = catscraper(offset=1,jump=8)
    b = time.time()
    images = c.getimages("owen wilson",10)
    print(images)
    e = time.time()
    print(f"Took {e-b} seconds to generate {len(images)} images")
    c.quit()



