__author__ = 'jquintanilla'
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(sum(map(ord, "aesthetics")))

def sinplot(flip=1):
    x = np.linspace(0, 14, 100)
    for i in range(1, 7):
        plt.plot(x, np.sin(x + i * .5) * (7 - i) * flip)

    sns.plt.show()

sinplot()