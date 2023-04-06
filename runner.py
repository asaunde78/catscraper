from CatScraper import catscraper

import concurrent.futures
import time

class scraper():
    def __init__(self, workers=1):
        self.workers = [catscraper(offset=wnum,jump=workers) for wnum in range(workers)]
        self.workercount = len(self.workers)
        pass
    def helper(self,tup):
        return self.worker_thread(tup[0],tup[1],tup[2])
    def worker_thread(self,workernum,search,number_of_images):
        
        kitty = self.workers[workernum]
        # print(kitty.__class__)
        images = kitty.find_image_urls(search,number_of_images)
        #imagelist = imagelist.extend(images)
        # del kitty
        return images
    def genimages(self,search,number_of_images):
        start = time.time()
        imagelist = []
        futures= []
        # number_of_images = 3
        

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workercount) as executor:
            w = [(wnum, search, number_of_images) for wnum in range(self.workercount)]
            print(w)
            results = executor.map(self.helper, w)
            for images in results:
                imagelist.extend(images)
        #     for worker in w:
        #         future = executor.submit(self.worker_thread,worker)
        #         futures.append(future)

        # for future in futures:
        #     images = future.result()
        #     imagelist.extend(images)


        finish = time.time()
        print(f"Took {finish-start} seconds")
        return imagelist
        
if __name__ == "__main__":
    s = scraper(workers=5)
    print(s.genimages("kalista",1))
    print(s.genimages("funny monkey",3))