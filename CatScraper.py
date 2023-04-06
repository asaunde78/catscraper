
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


        self.max_missed = 5
        self.driver.get("https://www.google.com/search")
        time.sleep(2)
    def quit(self):
        self.driver.quit()
    def getimages(self,search,num):
        start = time.time()
        time.sleep(0.10 * (self.offset))
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
    
        self.driver.get(f"{url}?{query_string}")
        # time.sleep(3)
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        highest_index = self.offset

        while len(image_urls) < num:
            
            thumbnails = self.driver.find_elements(By.CLASS_NAME,"bRMDJf")
            print(f"[LENGTH] Thumbnails length for {self.offset}: ", len(thumbnails))
            print(f"{self.offset} starting at {highest_index}")
            l = list(range(len(thumbnails)))
            print(f"{self.offset} looking at indexes {l[highest_index:][::self.jump]}")
            thumbnails = thumbnails[highest_index:][::self.jump]
            print(f"{self.offset} has {len(thumbnails)} to look at")
            for ind,nail in enumerate(thumbnails):
                
                print(f'{self.offset} found {nail.find_element(By.CLASS_NAME,"rg_i").get_attribute("alt")}')
                nail.click()
                class_name = "n3VNCb"
                wait = WebDriverWait(self.driver, 30)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
                
                images = self.driver.find_elements(By.CLASS_NAME, class_name)
                for image in images:
                    src_link = image.get_attribute("src")
                    # print(src_link)
                    # if(not("http" in  src_link) or not(not "encrypted" in src_link)):
                    #     print("BAD IMAGE WTF")
                    if(("http" in  src_link) and (not "encrypted" in src_link)):
                        print(
                            f"\t[LINK] \t {src_link}")
                        image_urls.append(src_link)
                        if len(image_urls) >= num:
                            return image_urls
                highest_index = highest_index + self.jump#*ind
                print(f"new highest index for {self.offset} is {highest_index}")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"{self.offset} is scrolling")
            time.sleep(5)
        # print("reached end :/")
        return image_urls
    def find_image_urls(self, search, num):
        
        start = time.time()
        time.sleep(0.250 * (self.offset))
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
        # time.sleep(3)
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        indx = 1
        print("ELEMENTS: ",len(self.driver.find_elements(By.CLASS_NAME,"bRMDJf")))
        while num > count:
            # time.sleep(1)
            begin = time.time()
            divindx = self.offset + self.jump*indx
            print(f"[divindx]: {divindx}")
            try:
                #find and click image
                
                imgurl = self.driver.find_element(By.XPATH,'//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'%(str(divindx)))
                
                # print(f"Worker:{self.offset} [IMGURL]: {imgurl}")
                # self.driver.execute_script("arguments[0].scrollIntoView(true);", imgurl)
                # time.sleep(1)
                imgurl.click()
                # time.sleep(1)
                wait = WebDriverWait(self.driver, 30)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

                missed_count = 0
            except Exception as e :
                # time.sleep(1)
                print("[ERROR] missed",e)
                missed_count = missed_count + 1
                if (missed_count>self.max_missed):
                    print("[INFO] Maximum missed photos reached, exiting...")
                    break

            try:
                
                class_name = "n3VNCb"
                images = self.driver.find_elements(By.CLASS_NAME, class_name)
            
                for image in images:

                    src_link = image.get_attribute("src")
                    # print(src_link)
                    # if(not("http" in  src_link) or not(not "encrypted" in src_link)):
                    #     print("BAD IMAGE WTF")
                    if(("http" in  src_link) and (not "encrypted" in src_link)):
                        print(
                            f"[INFO] {search} \t #{count} \t absolute: {self.offset + self.jump*indx} \t {src_link}")
                        image_urls.append(src_link)
                        count +=1
                        ending = time.time()
                        print(f"clicking took {ending-begin}")
                        break
            except Exception as e:
                # time.sleep(1)
                print(f"[ERROR] Unable to get link: ", e)
                print(traceback.format_exc())
            
            try:
                #scroll page to load next image
                if(count%3==0):
                    self.driver.execute_script("window.scrollTo(0, "+str((divindx)*60)+");")
                element = self.driver.find_element(By.CLASS_NAME,"mye4qd")
                element.click()
                print("[INFO] Loading next page")
                # time.sleep(3)
                wait = WebDriverWait(self.driver, 30)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            except Exception:
                time.sleep(1)
            indx += 1
            


        # self.driver.quit()
        print("[INFO] Google search ended")
        end = time.time()
        print(f"Took {end - start} seconds")
        # self.driver.quit()
        return image_urls
    
if __name__ == "__main__":
    # c = catscraper(offset=1,jump=2)
    c = catscraper(offset=1,jump=2)
    b = time.time()
    images = c.getimages("owen wilson",1)
    print(images)
    e = time.time()
    print(f"Took {e-b} seconds to generate {len(images)} images")
    c.quit()



