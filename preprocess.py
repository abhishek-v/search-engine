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
Remove self loops and dead-ends
'''

class Crawler:

    def __init__(self):
        self.page_count = 0
        '''WARNING: EXPLICIT MODIFICATION NEEDED FOR FOLLOWING TWO VARIABLES'''
        self.page_threshold = 200
        data_file = open("crawl_200","rb")
        self.link_reference = pickle.load(data_file)
        self.reverse_link_reference = pickle.load(data_file)
        self.nodes_inlink = dict()
        self.nodes_outlink = dict()
        #page rank graph having separate 2D dictionaries for inlinks and outlinks
        for index in self.link_reference.keys():
            self.nodes_inlink[index] = {}
            self.nodes_outlink[index] = {}
        print(self.link_reference)
        self.inv_index = {}
        self.ps = PorterStemmer()
        self.nodes_score = dict()
        self.nodes = dict()
        self.IDF = {}
        self.regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
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

        for index,value in self.link_reference.items():
            file = open("./data/"+str(index),"r")
            self.inv_index[index] = {}
            temp_word_list = [] #to make sure word is added to IDF only once for each page
            r = file.read()
            soup = BeautifulSoup(r, 'lxml')
            tags = soup.find_all('a')
            words = self.text_from_html(r)
            words = " ".join(re.findall("[a-zA-Z0-9]+", words)) #Only alphabets and numbers
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
                        if(temp_href in self.link_reference.values()):
                            #add in link and out link entries
                            temp_val = self.reverse_link_reference[temp_href]
                            self.nodes_outlink[index][temp_val] = self.nodes_outlink[index].get(temp_val,0) + 1
                            self.nodes_inlink[temp_val][index] = self.nodes_inlink[index].get(index,0) + 1
                except:
                    continue

            print("Processing file "+str(index)+" with URL: http://"+value)
        outfile = open("preprocess_"+str(self.page_threshold),"wb")
        pickle.dump(self.nodes_inlink, outfile)
        pickle.dump(self.nodes_outlink,outfile)
        pickle.dump(self.inv_index,outfile)
        pickle.dump(self.IDF,outfile)
        outfile.close()
        print("Successfully pickled the files")


if(__name__=="__main__"):
    c = Crawler()
    c.crawl()
    print("Terminating crawler")
