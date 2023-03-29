# https://archive.ics.uci.edu/ml/datasets/car+evaluation

import pandas as pd
import numpy as np
import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
from sklearn import linear_model,preprocessing

# get data
headers = [
"buying",   #:   vhigh, high, med, low.
"maint",    #:    vhigh, high, med, low.
"doors",    #:    2, 3, 4, 5more.
"persons",  #:  2, 4, more.
"lug_boot", #: small, med, big.
"safety",   #:   low, med, high.
"class"     # unacc, acc, good, vgood"
]

data = pd.read_csv(r"C:\Users\ahkar\OneDrive\Documents\UCI\cars\car.data",header=None,names=headers)
print(data.head())

# convert categorical data to numeric
le = preprocessing.LabelEncoder()

buying = le.fit_transform(list(data["buying"]))
maint = le.fit_transform(list(data["maint"]))
doors = le.fit_transform(list(data["doors"]))
persons = le.fit_transform(list(data["persons"]))
lug_boot = le.fit_transform(list(data["lug_boot"]))
safety = le.fit_transform(list(data["safety"]))
cls = le.fit_transform(list(data["class"]))

predict = "class"
X = list(zip(buying,maint,doors,persons,lug_boot,safety))
y = list(cls)

# split data
x_train,x_test,y_train,y_test =  sklearn.model_selection.train_test_split(X,y,test_size=0.1)

# fit classifier
K = 9
model = KNeighborsClassifier(n_neighbors=5)

model.fit(x_train,y_train)
acc = model.score(x_test,y_test)
print(acc)

# look at results
predicted = model.predict(x_test)
names = ["unacc","acc","good","vgood"]

for i in range(len(x_test)):
    print(f"predicted = {names[predicted[i]]}, data = {x_test[i]}, actual = {names[y_test[i]]}")
    n=model.kneighbors([x_test[i]],9,True)
    print(n)

