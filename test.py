import numpy as np

a = np.ones((3, 5, 5))

a = np.pad(a, pad_width=2, constant_values=2)

print(a)