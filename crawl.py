import requests
import os
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import deque
import re
import pickle
from urllib.parse import urlparse

'''
Crawling and downloading pages. Keep track of the N=3000 pages crawled.
'''

class Crawler:

    def __init__(self, url_list):
        self.page_count = 0
        self.URL_queue = deque()
        self.inv_index = {}
        self.link_reference = {}
        self.reverse_link_reference = {}
        '''EXPLICITLY SET VARIABLE'''
        self.page_threshold = 20 #increase limit
        self.regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        for URL in url_list:
            o = urlparse(URL)
            self.URL_queue.append((o.netloc+o.path).lstrip("www.").rstrip("/"))
        self.domain = "uic.edu"
        try:
            os.mkdir("data")
        except:
            #folder already exists
            pass

    def tag_visible(self,element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_html(self,body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

    def crawl(self):
        while(len(self.URL_queue) != 0):
            try:
                URL = self.URL_queue.popleft()
                r = requests.get("http://"+URL)
                if(r.status_code == 200):
                    self.link_reference[self.page_count] = URL
                    self.reverse_link_reference[URL] = self.page_count
                    soup = BeautifulSoup(r.text, 'lxml')
                    tags = soup.find_all('a')
                    for tag in tags:
                        try: #make sure there is a href tag. For <a class="", this will throw error. Hence, the try catch
                            if(re.match(self.regex, tag["href"]) is not None):
                                o = urlparse(tag["href"])
                                temp_href = ((o.netloc+o.path).lstrip("www.").rstrip("/"))
                                if(self.domain in tag["href"] and temp_href not in self.link_reference.values() and temp_href not in self.URL_queue):
                                    self.URL_queue.append(temp_href)
                        except:
                            continue
                    # print("LIST:\n\n",self.URL_queue)
                    '''save web page here'''
                    f = open("data/"+str(self.page_count),"w")
                    f.write(r.text)
                    f.close()
                    if(len(self.link_reference) > self.page_threshold):
                        outfile = open("crawl_"+str(self.page_threshold),"wb")
                        pickle.dump(self.link_reference,outfile)
                        pickle.dump(self.reverse_link_reference,outfile)
                        outfile.close()
                        print("Successfully pickled the files")
                        print("Page limit reached. Breaking..")
                        break

                    self.page_count += 1
                    print("Currently crawling page",URL)
                    if(self.page_count % 50):
                        print("TOTAL PAGES CRAWLED: ",str(self.page_count))
            except Exception as e:
                print(e)
                print("Connection failed for ", URL)
                continue


if(__name__=="__main__"):
    root_URL = ["http://www.cs.uic.edu"]
    c = Crawler(root_URL)
    c.crawl()
    print("Terminating crawler")
