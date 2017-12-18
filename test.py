import sys
import numpy as np
import cv2
import time



start_time = time.time()

im = cv2.imread('10h.png', 0)
ret, im = cv2.threshold(im,127,255,cv2.THRESH_BINARY_INV)

row_start = 0
for i in im:
    if np.sum(i) == 0:
        row_start += 1
    else:
        break

print(row_start)

im = im[row_start:]


c_start = 0
for c in im.T:
    if np.sum(c) == 0:
        c_start += 1
    else:
        break
print(c_start)
im = im[:, c_start:]

c_end = 0
for c in im.T:
    if np.sum(c) != 0:
        c_end += 1
    else:
        break

im = im[:, :c_end]

r_end = 0
for r in im[::-1]:
    if np.sum(i) == 0:
        r_end += 1
    else:
        break

im = im[::-1]
row_start = 0
for i in im:
    if np.sum(i) == 0:
        row_start += 1
    else:
        break

im = im[row_start:]
im = im[::-1]


print(im)
print(type(im))

print(im.shape)

print(time.time()-start_time)
cv2.imshow('window', im)

cv2.waitKey(0)
cv2.destroyAllWindows()


