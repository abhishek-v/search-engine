import numpy as np
import pickle
# from autocorrect import spell
from copy import deepcopy
import operator
from nltk.stem import PorterStemmer  # For Porter Stemmer function

if (__name__ == "__main__"):

    page_threshold = 5000
    data_file = open("crawl_5000", "rb")
    link_reference = pickle.load(data_file)
    data_file.close()
    # DO QUERY VALIDATION HERE
    q = input("Enter search query: ")
    q = q.split(" ")
    temp_q = ""
    ps = PorterStemmer()
    for word in q:
        # temp = spell(word)
        temp = word.lower()
        temp = ps.stem(temp)
        temp_q += (temp + " ")

    q = temp_q.rstrip(" ")
    # print("New user query is", temp_q.rstrip(" "))

    # print("Loading data files. Please wait.")
    ip = open("preprocess2_5000", "rb")
    stream_length_title = pickle.load(ip)
    stream_length = pickle.load(ip)
    IDF_title = pickle.load(ip)
    IDF = pickle.load(ip)

    inv_index_title = pickle.load(ip)
    inv_index = pickle.load(ip)
    TF_IDF_title = pickle.load(ip)
    TF_IDF = pickle.load(ip)
    no_slashes = pickle.load(ip)
    len_URL = pickle.load(ip)
    outlink_count = pickle.load(ip)
    inlink_count = pickle.load(ip)
    url_split = pickle.load(ip)
    ip.close()

    ip = open("pagerank_5000", "rb")
    page_rank = pickle.load(ip)

    #top 10 pages according to page rank
    # for i in range(0,50):
    #     print(i,page_rank[i][0], page_rank[i][1])
    #
    # exit()



    ip.close()

    IDF_q = 0  # global variable, constant for all documents in query
    IDF_q_title = 0
    # calculating IDF based on query terms
    for word in q:
        IDF_q += IDF.get(word, 0)
        IDF_q_title += IDF_title.get(word, 0)

    # calculate tf of body
    sum_tf = {}
    min_tf = {}
    max_tf = {}
    mean_tf = {}
    sum_url = {}
    covered_terms = {}

    for doc, word_map in inv_index.items():
        covered_terms[doc] = 0

    temp = q.split(" ")
    for word in temp:
        for doc, word_map in inv_index.items():
            # check number of occurences of query word in word_map
            sum_tf[doc] = sum_tf.get(doc, 0) + word_map.get(word, 0)
            if (word_map.get(word, 0) != 0):
                covered_terms[doc] = covered_terms.get(doc) + 1

            if (min_tf.get(doc, 0) == 0):
                min_tf[doc] = word_map.get(word, 0)
            else:
                if (min_tf[doc] > word_map.get(word, float("Inf"))):
                    min_tf[doc] = word_map.get(word)

            if (max_tf.get(doc, 0) == 0):
                max_tf[doc] = word_map.get(word, 0)
            else:
                if (max_tf[doc] < word_map.get(word, 0)):
                    max_tf[doc] = word_map.get(word, 0)

    '''printing and testing'''
    # count = 0
    # for doc,tf in sum_tf.items():
    #     print(covered_terms[doc])
    #     count = count + 1
    #     if(count > 100):
    #         break

    # exit()

    mean_tf = deepcopy(sum_tf)
    for doc, tf in mean_tf.items():
        if (covered_terms[doc] != 0):
            mean_tf[doc] /= covered_terms[doc]
        else:
            mean_tf[doc] = 0

    covered_term_ratio = {}
    for doc, freq in covered_terms.items():
        covered_term_ratio[doc] = freq / len(temp)

    # calculate tf of TITLE
    sum_tf_title = {}
    min_tf_title = {}
    max_tf_title = {}
    mean_tf_title = {}
    covered_terms_title = {}

    temp = q.split(" ")
    for doc, word_map in inv_index_title.items():
        covered_terms_title[doc] = 0
    for word in temp:
        for doc, word_map in inv_index_title.items():
            # check number of occurences of query word in word_map
            sum_tf_title[doc] = sum_tf_title.get(doc, 0) + word_map.get(word, 0)
            if (word_map.get(word, 0) != 0):
                covered_terms_title[doc] = covered_terms_title.get(doc) + 1

            if (min_tf_title.get(doc, 0) == 0):
                min_tf_title[doc] = word_map.get(word, 0)
            else:
                if (min_tf_title[doc] > word_map.get(word, float("Inf"))):
                    min_tf_title[doc] = word_map.get(word)

            if (max_tf_title.get(doc, 0) == 0):
                max_tf_title[doc] = word_map.get(word, 0)
            else:
                if (max_tf_title[doc] < word_map.get(word, 0)):
                    max_tf_title[doc] = word_map.get(word, 0)

    mean_tf_title = deepcopy(sum_tf_title)
    for doc, tf in mean_tf_title.items():
        if (covered_terms_title[doc] != 0):
            mean_tf_title[doc] /= covered_terms_title[doc]
        else:
            mean_tf_title[doc] = 0

    covered_term_ratio_title = {}
    for doc, freq in covered_terms_title.items():
        covered_term_ratio_title[doc] = freq / len(temp)

    '''


    TF-IDF OF TITLE


    '''
    sum_tf_idf_title = {}
    min_tf_idf_title = {}
    max_tf_idf_title = {}
    mean_tf_idf_title = {}
    for word in temp:
        for doc, word_map in TF_IDF_title.items():
            # check number of occurences of query word in word_map
            sum_tf_idf_title[doc] = sum_tf_idf_title.get(doc, 0) + word_map.get(word, 0)

            if (min_tf_idf_title.get(doc, 0) == 0):
                min_tf_idf_title[doc] = word_map.get(word, 0)
            else:
                if (min_tf_idf_title[doc] > word_map.get(word, float("Inf"))):
                    min_tf_idf_title[doc] = word_map.get(word)

            if (max_tf_idf_title.get(doc, 0) == 0):
                max_tf_idf_title[doc] = word_map.get(word, 0)
            else:
                if (max_tf_idf_title[doc] < word_map.get(word, 0)):
                    max_tf_idf_title[doc] = word_map.get(word, 0)

    mean_tf_idf_title = deepcopy(sum_tf_idf_title)
    for doc, tf in mean_tf_idf_title.items():
        if (covered_terms_title[doc] != 0):
            mean_tf_idf_title[doc] /= covered_terms_title[doc]
        else:
            mean_tf_idf_title[doc] = 0

    '''


        TF-IDF OF BODY


    '''
    sum_tf_idf = {}
    min_tf_idf = {}
    max_tf_idf = {}
    mean_tf_idf = {}
    for word in temp:
        for doc, word_map in TF_IDF.items():
            # check number of occurences of query word in word_map
            sum_tf_idf[doc] = sum_tf_idf.get(doc, 0) + word_map.get(word, 0)

            if (min_tf_idf.get(doc, 0) == 0):
                min_tf_idf[doc] = word_map.get(word, 0)
            else:
                if (min_tf_idf[doc] > word_map.get(word, float("Inf"))):
                    min_tf_idf[doc] = word_map.get(word)

            if (max_tf_idf.get(doc, 0) == 0):
                max_tf_idf[doc] = word_map.get(word, 0)
            else:
                if (max_tf_idf[doc] < word_map.get(word, 0)):
                    max_tf_idf[doc] = word_map.get(word, 0)

    mean_tf_idf = deepcopy(sum_tf_idf)
    for doc, tf in mean_tf_idf.items():
        if (covered_terms[doc] != 0):
            mean_tf_idf[doc] /= covered_terms[doc]
        else:
            mean_tf_idf[doc] = 0

    # '''printing and testing'''
    # count = 0
    # for doc,tf in mean_tf_idf.items():
    #     print(mean_tf_idf[doc])
    #     count = count + 1
    #     if(count > 100):
    #         break
    # exit()

    # accepted_features = [1,3,5,6,8,10,11,13,15,16,18,20,21,23,25,26,28,30,31,33,35,36,38,40,71,73,75,76,78,80,81,83,85,88,90,126,127,128,129,130]
    accepted_features = [3, 5, 8, 10, 13, 15, 18, 20, 23, 25, 28, 30, 33, 35, 38, 40, 73, 75, 78, 80, 83, 85, 88, 90,
                         126, 127, 128, 129, 130]
    accepted_features = list(map(str, accepted_features))

    # LOAD AND RUN NEURAL NETWORK

    # model = load_model("ltr_model.h5")
    rank = {}

    # count = 0
    # for doc in inv_index.keys():
    #     print(link_reference[doc],sum_tf[doc], min_tf[doc], max_tf[doc], covered_term_ratio[doc])
    #     count = count + 1
    #     if(count > 100):
    #         break
    #
    # exit()

    for word in temp:
        for doc, word_map in url_split.items():
            # check number of occurences of query word in word_map
            sum_url[doc] = sum_url.get(doc, 0) + word_map.get(word, 0)
    # assigning weights manually between values 0 - 1


    max_inlink = max(inlink_count.items(), key=operator.itemgetter(1))[1]

    print("Results WITH intelligent component:")
    for doc in inv_index.keys():

        # loop through all pages , feed into neural net and predict values
        ip = []
        ip.append(40*covered_terms_title[doc])
        ip.append(100*covered_terms[doc])

        ip.append(40*covered_term_ratio_title[doc])
        ip.append(100*covered_term_ratio[doc])
        try:
            ip.append(0.0001*stream_length_title[doc])
        except:
            ip.append(0)
        ip.append(0*stream_length[doc])

        ip.append(0.01*IDF_q_title)
        ip.append(0.01*IDF_q)

        ip.append(1*sum_tf_title[doc])
        ip.append(0.001*sum_tf[doc])

        ip.append(0.01*min_tf_title[doc])
        ip.append(0.01*min_tf[doc])

        ip.append(0.01*max_tf_title[doc])
        ip.append(0.01*max_tf[doc])

        ip.append(0.01*mean_tf_title[doc])
        ip.append(0.01*mean_tf[doc])

        ip.append(0.001*sum_tf_idf_title[doc])
        ip.append(0.001*sum_tf_idf[doc])

        ip.append(0.01*min_tf_idf_title[doc])
        ip.append(0.01*min_tf_idf[doc])

        ip.append(0.01*max_tf_idf_title[doc])
        ip.append(0.01*max_tf_idf[doc])

        ip.append(0.01*mean_tf_idf_title[doc])
        ip.append(0.01*mean_tf_idf[doc])

        ip.append(-1*2*no_slashes[doc])
        ip.append(-1*1*len_URL[doc])

        #ip.append(0.0001*covered_terms[doc]*10*inlink_count[doc])
        ip.append((inlink_count[doc]/max_inlink)*110)
        ip.append(0.00001*outlink_count[doc])
        #ip.append(120 - page_rank[doc]/41.6)
        a = ((5000 - page_rank[doc])/5000) * 110
        ip.append(a)

        # ip.append(30 * sum_url[doc])
        # if(covered_terms[doc]>0):
        #     print("Document number:",doc)
        #     print(link_reference[doc])
        #     print(ip)
        #     print(sum(ip))
        # ip = np.asarray(ip)

        # if (link_reference[doc] == "cs.uic.edu/faculty"):
        #     print(link_reference[doc])
        #     print(page_rank[doc])
        #     print(ip)
        #     print(sum(ip))
        #
        # if (link_reference[doc] == "cs.uic.edu/~cornelia"):
        #     print(page_rank[doc])
        #     print(link_reference[doc])
        #     print(ip)
        #     print(sum(ip))
        #
        # if (link_reference[doc] == "uic.edu/apps/departments-az/search"):
        #     print(page_rank[doc])
        #     print(link_reference[doc])
        #     print(ip)
        #     print(sum(ip))
        #
        # if (link_reference[doc] == "uic.edu"):
        #     print(link_reference[doc])
        #     print(page_rank[doc])
        #     print(ip)
        #     print(sum(ip))
        ip = sum(ip)



        rank[doc] = ip

    page_order = sorted(rank.items(), key=lambda kv: kv[1], reverse=True)
    # print(page_order)
    print("The top 10 search results are:")
    for i in range(0, 10):
        try:
            print(link_reference[page_order[i][0]])
        except:
            print("Unknown page")



    print("\n\nResults WITHOUT intelligent component:")
    for doc in inv_index.keys():

        # loop through all pages , feed into neural net and predict values
        ip = []
        ip.append(40*covered_terms_title[doc])

        ip = sum(ip)



        rank[doc] = ip

    page_order = sorted(rank.items(), key=lambda kv: kv[1], reverse=True)
    # print(page_order)
    print("The top 10 search results are:")
    for i in range(0, 10):
        try:
            print(link_reference[page_order[i][0]])
        except:
            print("Unknown page")