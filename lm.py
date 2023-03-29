# https://archive.ics.uci.edu/ml/datasets/Student+Performance
import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

from sklearn import linear_model
from sklearn.utils import shuffle

# get data
data = pd.read_csv(r"C:\Users\ahkar\OneDrive\Documents\UCI\student\student-mat.csv",sep=";")
data = data[["G1","G2","G3","studytime","failures","absences"]]

# fit model
predict = "G3"
X=np.array(data.drop([predict],1))
y=np.array(data[predict])
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)

"""
best = 0
for _ in range(99):
    # gen data
    x_train,x_test,y_train,y_test=sklearn.model_selection.train_test_split(X,y,test_size=0.1)

    # fit model
    linear = linear_model.LinearRegression()
    linear.fit(x_train,y_train)

    acc = linear.score(x_test, y_test)

    if (acc > best):
        # save model
        with open("student_model.pkl","wb") as f:
            pickle.dump(linear,f)

        best = acc
        print(acc)
"""

# load best model
with open("student_model.pkl","rb") as f:
    linear = pickle.load(f)

# inspect
print(f"coef {linear.coef_}")
print(f"intercept {linear.intercept_}")

predictions = linear.predict(x_test)

# inspect
for i in range(len(predictions)):
    print(predictions[i],y_test[i],x_test[i])

# plot
style.use("ggplot")
p="failures"
plt.scatter(data[p],data[predict])
plt.xlabel(p)
plt.ylabel(predict)
plt.show()