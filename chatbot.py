import nltk
# nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle

with open("chatbot_intents.json") as f:
    data = json.load(f)

##################################################################
# prep data
##################################################################
try:
    with open("chatbot_data.pkl","rb") as f:
        words,labels,training,output = pickle.load(f)
except:
    # scrape json data
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        #print(f"intent = {intent}")
        for pattern in intent["patterns"]:
            #print(f"\tpattern = {pattern}")
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    #print(f"docs_x = {docs_x}")
    #print(f"docs_y = {docs_y}")

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    # print(f"words = {words}")

    labels = sorted(labels)
    #print(f"labels = {labels}")

    # bag of words
    # onehot encoding

    # nn cant take words, needs numbers

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for i,doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[i])] = 1

        #print(f"bag = {bag}")
        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open("chatbot_data.pkl","wb") as f:
        pickle.dump((words,labels,training,output),f)

##################################################################
# set up NN
##################################################################
#tf.reset_default_graph() # depreciated
net = tflearn.input_data(shape=[None,len(training[0])])
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,len(output[0]),activation="softmax") # probability estimate
net = tflearn.regression(net)
model = tflearn.DNN(net)

##################################################################
# fit / get model
##################################################################
try:
    model.load("chatbot_model.tflearn.h5")
except:
    model.fit(training,output,n_epoch=1000,batch_size=8,show_metric=True)
    model.save("chatbot_model.tflearn.h5")

#print(training)
#print(output)

##################################################################
# make predictions
##################################################################

# take sentence and make it a bag of words
def bag_of_words(s,words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i,w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

def chat():
    print("start talking with bot (type 'quit' to exit)")
    while True:
        inp = input("you: ")
        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp,words)])
        #print(results)

        results_index = np.argmax(results)

        tag = labels[results_index]

        for tg in data["intents"]:
            if tg["tag"] == tag:
                responses = tg["responses"]

        print(random.choice(responses))

chat()