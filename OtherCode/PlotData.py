# plot csv data from folder "Updated Data" and the file name "Data.csv"

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

folder_name = "Updated Data"
original_filename = "data.csv"

data = pd.read_csv(os.path.join(folder_name, original_filename))

plt.plot(data['x'], data['y'])
plt.show()

print(data['x'].iloc[0])
print(data['x'].iloc[-1])