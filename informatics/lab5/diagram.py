import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("data.csv")

data = data.groupby(['<DATE>'])

data.boxplot(
    column=["<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>"], 
    grid=True, 
    patch_artist=True, 
    boxprops=dict(facecolor="lightblue")
)

plt.show()