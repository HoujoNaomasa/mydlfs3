if '__file__' in globals():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from statistics import variance
from tkinter import W
import numpy as np
from dezero import Variable
import dezero.functions as F
from dezero.core import as_variable

# dataset
np.random.seed(0)
x = np.random.rand(100, 1)
y = np.sin(2 * np.pi * x) + np.random.rand(100, 1)

# initilize W
I, H, O = 1, 10, 1
W1 = Variable(0.01 * np.random.randn(I, H))
b1 = Variable(np.zeros(H))
W2 = Variable(0.01 * np.random.randn(H, O))
b2 = Variable(np.zeros(O))

# suiron

def predict(x):
    y = F.linear_simple(x, W1, b1)
    y = F.sigmoid_simple(y)
    y = F.linear_simple(y, W2, b2)
    return y


lr = 0.2
iters = 10000

# gakusyuu
for i in range(iters):
    y_pred = predict(x)
    loss = F.mean_squared_error(y, y_pred)

    W1.clearngrad()
    b1.clearngrad()
    W2.clearngrad()
    b2.clearngrad()
    loss.backward()

    W1.data -= lr * W1.grad.data
    b1.data -= lr * b1.grad.data
    W2.data -= lr * W2.grad.data
    b2.data -= lr * b2.grad.data
    if i  % 1000 == 0:
        print(loss)