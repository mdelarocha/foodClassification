#!/usr/bin/python2.7
import cv2
import os
import os.path
import glob
import numpy as np

path = 'photos/'
outPath = path + "resized/"

files = ['4I0NkNy1dY_5FQyzqug_3A.jpg', '8oNMERBv446CP4OIylRSUA.jpg' , 'DGn5tSx9odNMPQvRIfj-zg.jpg', '_GJxADNrH_2glXoP_miPpw.jpg', 'dposta3m3NTwG8hKwfBd5Q.jpg', '-kgvlEq23tGgjW2ZL4CMMQ.jpg']

xRes = 128
yRes = 128

#open images
for i in range(0,6):
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


