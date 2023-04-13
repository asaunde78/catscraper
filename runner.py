from CatScraper import catscraper

import concurrent.futures
import time
import subprocess
from multiprocessing import Process

import sys,requests
#LINUX 
sys.path.insert(1, '/home/asher/linkdownloadersite')
sys.path.insert(1, '/home/asher/catscraper/blockerextension.crx')
from linkdownloader import downloader

#WINDOWS
# sys.path.insert(1, '/blockerextension.crx')
# sys.path.insert(1, '/Users/Asher/Downloads/code/linkdownloadersite')

# subprocess.run(["pkill", "chrome"])
class scraper():
    
    def __init__(self, workers=1,folder="images",server=False):
        #UNCOMMENT THIS FOR LINUX
        subprocess.run(["pkill", "chrome"])
        self.folder=folder
        print("generating workers...")
        self.workers = [catscraper(offset=wnum,jump=workers) for wnum in range(workers)]
        self.workercount = len(self.workers)
        # self.downloader = downloader()
        # self.downloader.run(port=6969)
        self.server=server
        #UNCOMMENT THIS FOR DOWNLOAD SERVER 
        if(self.server):
            print("starting downloadserver")
            self.downloader = downloader(folder=self.folder,fixname=False)
            self.downloaderprocess = Process(target=self.downloader.run)
            self.downloaderprocess.start()

    def kill(self):
        
        for worker in self.workers:
            worker.quit()
        #UNCOMMENT THIS FOR DOWNLOAD SERVER
        if(self.server):
            # time.sleep(3)
            self.downloaderprocess.terminate()
            self.downloaderprocess.join()

    def helper(self,tup):
        return self.worker_thread(tup[0],tup[1],tup[2],tup[3])
    def worker_thread(self,workernum,search,number_of_images,filetype):
        kitty = self.workers[workernum]
        images = kitty.getimages(search,number_of_images,filetype)
        return images
    def genimages(self,search,number_of_images,divide=False,filetype=None):
        start = time.time()
        imagelist = []
        
        # number_of_images = 3
        requests.get(f"http://localhost:6969/kill")

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workercount) as executor:
            workers = self.workercount
            imagenum = number_of_images

            if(divide):
                w = [[wnum, search, 0,filetype] for wnum in range(self.workercount)]
                for x in range(workers):
                    main = imagenum//workers
                    if main < imagenum:

                        w[x][2] = main
                    else:
                        w[x][2] = imagenum
                    workers -= 1
                    imagenum -= main
                print(w)
                w = [tuple(a)for a in w]
            else:
                w = [(wnum, search, number_of_images,filetype) for wnum in range(self.workercount)]

            #print(w)
            results = executor.map(self.helper, w)
            for images in results:
                imagelist.extend(images)
    
        finish = time.time()
        print(f"Took {finish-start} seconds")
        time.sleep(1)
        return imagelist
        
if __name__ == "__main__":
    s = scraper(workers=2,server=False)
    # print(s.genimages("funny monkey",1))
    s.genimages("funny monkey",1)
    # time.sleep(2)
    b = time.time()
    workoutputs = s.genimages("funny doggy",20)
    print(workoutputs)
    e = time.time()
    print(f"Took {e-b} seconds to generate and download the images")
    # workoutputs = s.genimages("funny minions",1)
    s.kill()