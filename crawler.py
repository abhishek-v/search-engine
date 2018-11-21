import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import deque
import nltk
from nltk.corpus import stopwords
import re
from nltk.stem import PorterStemmer #For Porter Stemmer function
import pickle
from urllib.parse import urlparse
#Branch BS
'''
Need to add page rank
'''

class Crawler:

    def __init__(self, url_list):
        self.page_count = 0
        self.URL_queue = deque()
        self.inv_index = {}
        self.link_reference = {}
        self.ps = PorterStemmer()
        self.nodes_score = dict()
        self.nodes = dict()
        self.IDF = {}
        self.page_threshold = 1000 #increase limit
        self.regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        for URL in url_list:
            o = urlparse(URL)
            self.URL_queue.append((o.netloc+o.path).lstrip("www.").rstrip("/"))
        self.domain = "uic.edu"
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))

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
                    self.inv_index[self.page_count] = {}
                    self.link_reference[self.page_count] = URL
                    temp_word_list = [] #to make sure word is added to IDF only once for each page
                    soup = BeautifulSoup(r.text, 'lxml')
                    tags = soup.find_all('a')
                    words = self.text_from_html(r.text)
                    words = " ".join(re.findall("[a-zA-Z0-9]+", words)) #Only alphabets
                    words = words.split(" ")
                    for word in words:
                        #preprocess each word
                        if(word not in self.stop_words):
                            word = word.lstrip(" ")
                            word = word.rstrip(" ")
                            word = word.lower()
                            word = self.ps.stem(word)
                            #valid word. add it to inverted index
                            self.inv_index[self.page_count][word] = self.inv_index[self.page_count].get(word,0) + 1
                            if(word not in temp_word_list):
                                self.IDF[word] = self.IDF.get(word,0) + 1
                            temp_word_list.append(word)
                    temp_word_list = []
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
                    if(len(self.link_reference) > self.page_threshold):
                        outfile = open("data_"+str(self.page_threshold),"wb")
                        pickle.dump(self.inv_index, outfile)
                        pickle.dump(self.link_reference,outfile)
                        pickle.dump(self.IDF,outfile)
                        pickle.dump(self.page_count,outfile)
                        outfile.close()
                        print("Successfully pickled the files")
                        print("Page limit reached. Breaking..")
                        break

                    self.page_count += 1
                    print("URL is: ",URL)
                    print("Number of nodes in the graph is:",len(self.link_reference.keys()))
            except Exception as e:
                print(e)
                print("Connection failed for ", URL)
                continue


if(__name__=="__main__"):
    root_URL = ["http://www.cs.uic.edu"]
    c = Crawler(root_URL)
    c.crawl()
    print("Terminating crawler")
