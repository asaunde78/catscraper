from CatScraper import catscraper

import concurrent.futures
import time
import subprocess
# subprocess.run(["pkill", "chrome"])
class scraper():
    def __init__(self, workers=1):
        # subprocess.run(["pkill", "chrome"])
        self.workers = [catscraper(offset=wnum,jump=workers) for wnum in range(workers)]
        self.workercount = len(self.workers)
        pass
    def kill(self):
        for worker in self.workers:
            worker.quit()
    def helper(self,tup):
        return self.worker_thread(tup[0],tup[1],tup[2])
    def worker_thread(self,workernum,search,number_of_images):
        
        kitty = self.workers[workernum]
        # print(kitty.__class__)
        images = kitty.getimages(search,number_of_images)
        #imagelist = imagelist.extend(images)
        # del kitty
        return images
    def genimages(self,search,number_of_images,divide=False):
        start = time.time()
        imagelist = []
        
        # number_of_images = 3
        

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workercount) as executor:
            workers = self.workercount
            imagenum = number_of_images

            if(divide):
                w = [[wnum, search, 0] for wnum in range(self.workercount)]
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
                w = [(wnum, search, number_of_images) for wnum in range(self.workercount)]

            #print(w)
            results = executor.map(self.helper, w)
            for images in results:
                imagelist.extend(images)
    
        finish = time.time()
        print(f"Took {finish-start} seconds")
        return imagelist
        
if __name__ == "__main__":
    s = scraper(workers=2)
    s.genimages("funny",1)
    b = time.time()
    images = s.genimages("owen wilson",6)
    print(images)
    e = time.time()
    print(f"Took {e-b} seconds to generate {len(images)} images")
    print(f"There are {len(set(images))} unique pictures")
    s.kill()