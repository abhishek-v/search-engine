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
from copy import deepcopy

'''
Need to add page rank
Remove self loops and dead-ends
'''

class PageRank:
    def __init__(self):
        '''WARNING: EXPLICIT MODIFICATION NEEDED FOR FOLLOWING VARIABLE'''
        self.page_threshold = 5000
        data_file = open("crawl_"+str(self.page_threshold),"rb")
        self.link_reference = pickle.load(data_file)
        self.reverse_link_reference = pickle.load(data_file)
        data_file.close()
        data_file = open("preprocess_"+str(self.page_threshold),"rb")
        self.nodes_inlink = pickle.load(data_file)
        self.nodes_outlink = pickle.load(data_file)
        self.inv_index = pickle.load(data_file)
        self.IDF = pickle.load(data_file)
        data_file.close()
        self.nodes_score = {}
        self.dampFactor = 0.85
        self.nodeCount = len(self.link_reference.keys())


    def pagerank(self):
        #initialize page rank
        init_score = 1/self.nodeCount
        for index,value in self.link_reference.items():
            self.nodes_score[index] = init_score

        #DEADENDS
        # print("outgoing",self.nodes_outlink.items())
        nodes_no_outlinks = []
        for index,value in self.nodes_outlink.items():
            if(value == {}):
                nodes_no_outlinks.append(index)


        #algorithm starts here
        temp_score = deepcopy(self.nodes_score)
        iterations = 30
        for i in range(iterations):
            self.validate()
            dp = 0
            for node in nodes_no_outlinks:
                dp += (0.85 * (self.nodes_score[node]/self.nodeCount))
            for index in self.link_reference.keys(): #loop through each node and calculate its page rank
                #page rank formula:
                temp_score[index] = (self.dampFactor * self.formula(index)) + ((1-self.dampFactor)/self.nodeCount) + dp
            self.nodes_score = deepcopy(temp_score)


    def formula(self, curNode):
        score = 0
        for neighbour,value in self.nodes_inlink[curNode].items():
            numerator = self.nodes_score[neighbour]
            denominator = self.nodes_outlink[neighbour].keys()
            denominator = len(denominator)
            score += (numerator/denominator)
        return score

    def validate(self):
        sum = 0
        for index,value in self.nodes_score.items():
            sum = sum + (value)
        print(sum)


if(__name__=="__main__"):
    pr = PageRank()
    pr.pagerank()

    # pickle.dump(pr.nodes_score, outfile)
    page_rank = {}
    page_order = sorted(pr.nodes_score.items(), key=lambda kv: kv[1], reverse=True)

    rank = 1
    for page in page_order:
        page_rank[page[0]] = rank
        rank = rank + 1
    outfile = open("pagerank_"+str(pr.page_threshold),"wb")
    pickle.dump(page_rank, outfile)
    outfile.close()
    print("Terminating PageRank program")
