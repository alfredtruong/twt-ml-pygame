import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras_preprocessing.sequence import pad_sequences

#pip install numpy==1.16.1

train_model = False
n_words = 88000

data = keras.datasets.imdb
(train_data,train_labels),(test_data,test_labels) = data.load_data(num_words = n_words)

#print(train_data)
#print(train_labels)

# get word mapping
word_index = data.get_word_index()
word_index = {k:(v+3) for k,v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

reverse_word_index = dict([v,k] for k,v in word_index.items())
reverse_word_index

def decode_review(text):
    return " ".join([reverse_word_index.get(word,"?") for word in text])

decode_review(test_data[0])

# check that
#print(len(test_data[0]))
#print(len(test_data[1]))

# trim data to same size
train_data = pad_sequences(train_data,value=word_index["<PAD>"],padding="post",maxlen=250)
test_data = pad_sequences(test_data,value=word_index["<PAD>"],padding="post",maxlen=250)

#print(len(test_data[0]))
#print(len(test_data[1]))

# model here
if (train_model):
    model = keras.Sequential() # container
    model.add(keras.layers.Embedding(n_words,16)) # groups words together, generates word vectors, 16 diml, maps words to vectors
    model.add(keras.layers.GlobalAveragePooling1D()) # dimensional reduction
    model.add(keras.layers.Dense(16,activation="relu"))
    model.add(keras.layers.Dense(1,activation="sigmoid")) # not multiclass
    model.summary()

    model.compile(optimizer="adam",loss="binary_crossentropy",metrics=["accuracy"])

    # get validation data
    x_val = train_data[:10000]
    y_val = train_labels[:10000]

    x_train = train_data[10000:]
    y_train = train_labels[10000:]

    fitModel = model.fit(x_train,y_train,epochs=40,batch_size=512,validation_data=(x_val,y_val),verbose=1)

    # training acc > test acc
    results = model.evaluate(test_data,test_labels)
    print(results) # loss vs accuracy


    # save model
    model.save("model.h5")

    # examine single review
    test_review = test_data[0]
    predict = model.predict([test_review])
    print("review:")
    print(decode_review(test_review))
    print(f"prediction: {predict[0]}")
    print(f"actual: {test_labels[0]}")
else:
    model = keras.models.load_model("model.h5")

