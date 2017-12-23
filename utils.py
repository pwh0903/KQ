import numpy as np


def cut_blank(im):
    r_start = 0
    for i in im:
        if np.sum(i) == 0:
            r_start += 1
        else:
            break

    im = im[r_start:]

    r_end = 0
    for i in im:
        if np.sum(i) != 0:
            r_end += 1
        else:
            break

    im = im[:r_end]

    c_start = 0
    for c in im.T:
        if np.sum(c) == 0:
            c_start += 1
        else:
            break
    im = im[:, c_start:]

    c_end = 0
    for c in im.T:
        if np.sum(c) != 0:
            c_end += 1
        else:
            break
    im = im[:, :c_end]

    return im
