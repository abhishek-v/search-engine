import requests


class Crawler:

    def __init__(self, url_list):
        self.root_URL = url_list
        self.URL_queue = []

    def crawl(self):
        for URL in self.root_URL:
            self.URL_queue.append(URL)
        for URL in self.URL_queue:
            r = requests.get(URL)
            self.parse_HTML(r.text)
            exit(1)

    def parse_HTML(self,text):
        target = "<a href=\""
        domain = ".uic.edu"
        #comment
        l = len(target)
        idx = 0
        flag = 0
        cur_link = ""
        for ch in text:
            if(flag == 1):
                if(ch != "\""):
                    cur_link += ch
                    self.URL_queue.append(cur_link)
                    continue
                else:
                    flag = 0
                    print(cur_link)
                    cur_link = ""
                    idx = 0
                    continue
            if(ch == target[idx]):
                idx += 1
                if(idx == l):
                    flag = 1
                    idx = 0
                    continue
            else:
                idx = 0
if(__name__=="__main__"):
    root_URL = ["http://www.cs.uic.edu"]
    c = Crawler(root_URL)
    c.crawl()
