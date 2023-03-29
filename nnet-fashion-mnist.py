import sklearn.model_selection
import tensorflow as tf
from tensorflow import keras # api for tensorflow, high level api
import numpy as np
import matplotlib.pyplot as plt

data = keras.datasets.fashion_mnist

(train_images,train_labels),(test_images,test_labels) = data.load_data()
print(train_labels)

str="""0	T-shirt/top
1	Trouser
2	Pullover
3	Dress
4	Coat
5	Sandal
6	Shirt
7	Sneaker
8	Bag
9	Ankle boot"""
class_names = [x.split('\t')[1] for x in str.split('\n')]
class_names

# raw data
plt.imshow(train_images[7],cmap=plt.cm.binary)
print(train_images[7])

# scaled image to [0/1]
train_images = train_images/255.0 # normalize
test_images = test_images/255.0 # normalize

train_images[0].shape

# flatten array of arrays to simple array
model = keras.Sequential(
    [
        keras.layers.Flatten(input_shape=(28,28)),
        keras.layers.Dense(128,activation="relu"),
        keras.layers.Dense(10, activation="softmax"), # output class probabilities
    ]
)

model.compile(optimizer="adam",loss="sparse_categorical_crossentropy",metrics=["accuracy"])

model.fit(train_images,train_labels,epochs=10)
test_loss,test_acc = model.evaluate(test_images,test_labels)
print(f"tested acc = {test_acc}")

# do predictions
prediction = model.predict(test_images)
print(prediction[0])
print(class_names[np.argmax(prediction[0])])

plt.imshow(test_images[0])


for i in range(5):
    plt.grid(False)
    plt.imshow(test_images[i],cmap=plt.cm.binary)
    plt.xlabel("actual = " + class_names[test_labels[i]])
    plt.title("prediction = " + class_names[np.argmax(prediction[i])])
    plt.show()