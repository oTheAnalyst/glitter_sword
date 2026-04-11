import pandas as ps
import numpy as np
import requests as rq

a2 = np.array([1, 2, 3, 4, 5])
a2.shape


row_vector = a2[np.newaxis, :]
row_vector.shape



col_vector = a2[:, np.newaxis]
