import numpy as np

data = np.array([4, 14, 21, 2, 8, 16, 3, 15, 1, 7, 0, 6, 2, 1, 17, 2, 20, 30, 5, 1, 1, 3, 5, 14, 2, 18, 5, 7, 6])

# Calculate statistics
mean = np.mean(data)
median = np.median(data)
std_dev = np.std(data)

print("Mean:", mean)
print("Median:", median)
print("Standard Deviation:", std_dev)
