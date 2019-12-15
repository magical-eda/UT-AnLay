#
# @file util.py
# @author Mingjie Liu
# @date July 2019
# @brief generate coordinate channel embeddings
#

import numpy as np

# Coordinate channel embeddings

def cordinate_img(img):
    # img shape (dim, dim, chan)
    new_img_x = np.zeros((img.shape))
    new_img_y = np.zeros((img.shape))
    for x,y,c in list(zip(*np.where(img>0))):
        new_img_x[x,y,c] = x + 1
        new_img_y[x,y,c] = y + 1
    return new_img_x, new_img_y

