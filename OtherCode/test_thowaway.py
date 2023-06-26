import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

file_path = "D:/InteractivePlots/DataFolder/mpFiles/elbrest-abd-add-06-04-2023-15-17-34/images/06-04-2023-15-17-46-304.jpg"

# load a file with path file_path and show it
img = plt.imread(file_path)
plt.imshow(img)
plt.show()
