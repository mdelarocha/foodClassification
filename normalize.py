# Import Libraries

import cv2
import os
import os.path
import numpy as np

# Set the path

path = '/FileStore/tables/photosSample'
outPath = path + "resizedImgs/"

files = os.listdir(path)

xRes = 256
yRes = 256

# open images

for i in files:
    if not os.path.isfile(path + files[i]):
        print("File " + path + files[i] + " doesn't exist")
    else:
        print("Found file " + path + files[i])

img = cv2.imread(path + files[i])
cv2.imshow('original', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#now we crop it into a square

y, x, c = img.shape

if x > y:
    offset = (x-y)/2
    cropped = img[0:y, offset:(x-offset)]
elif y > x:
    offset = (y-x)/2
    cropped = img[offset:(y-offset), 0:x]
else:
    cropped = img;

#now we resize it to a standard resolution

imgOut = np.zeros((xRes, yRes, 3), np.uint8)
imgOut = cv2.resize(cropped, (xRes, yRes), 0, 0, cv2.INTER_LINEAR)
cv2.imshow('cropped', imgOut)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite(outPath + files[i], imgOut)

print("Wrote file " + outPath + files[i])
