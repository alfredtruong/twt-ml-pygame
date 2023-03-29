from time import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

np.random.seed(42)

digits = load_digits()
data = scale(digits.data) # 0 to 1

n_samples,n_features = data.shape
n_digits = len(np.unique(digits.target))
labels = digits.target

sample_size = 300

print(f"n digits = {n_digits}, n_samples = {n_samples}, n_features = {n_features}")

k=10
