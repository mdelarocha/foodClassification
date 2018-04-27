#!/usr/bin/python2.7
import cv2
import os
import os.path
import numpy as np
import pandas as pd
import shutil 
from pandas.io.json import json_normalize
from shutil import copyfile

#Written by Andrew McCament

#path for the normalized images
outPath = "photos/resized/"

#path for taking a sample of images
path  = "sample5000/"


print("Discovering files...");
files = os.listdir(path)

xRes = 256
yRes = 256


#open images, crop to square AR, resize to 256x256, save 
for i in range(0,len(files)):
	if not os.path.isfile(path + files[i]):
		print("File " + path + files[i] + " doesn't exist")
	elif files[i].endswith(".jpg"):
		print("Found jpeg file " + str(i) + ", " + path + files[i])

		#load image into openCV
		img = cv2.imread(path + files[i])

		#now we crop it into a square.  sometimes there are attribute errors from some 			files, so we catch that error
		try:
			y, x, c = img.shape
			if x > y:
				offset = (x-y)/2
				cropped = img[0:y, offset:(x-offset)] 
			elif y > x:
				offset = (y-x)/2
				cropped = img[offset:(y-offset), 0:x]
			else:
				cropped = img;

			#now we resize it to xRes by yRes
			imgOut = np.zeros((xRes, yRes, 3), np.uint8)
			imgOut = cv2.resize(cropped, (xRes, yRes), 0, 0, cv2.INTER_LINEAR)
	
			cv2.imwrite(outPath + files[i], imgOut)
		
			print("Wrote file " + outPath + files[i])

		except AttributeError:
			print("Attribute error!")

#now we filter each image by its label
print("Discovering normalized images")
normalized = os.listdir(outPath)

for i in range(0, len(normalized)):
	normalized[i] = normalized[i].replace(".jpg", "")

print("Loading JSON...")

labels = pd.read_json('photos.json', lines=True, orient='columns')

#now the data is in df labels
#so we go through each file and find the label
sortedFP = "normalized/"

#where the actual work happens for sorting and classifying
for i in range(0, len(normalized)):
	if normalized[i] in labels.values:
		index = labels[labels['photo_id'] == normalized[i]].index.item()

		thisLabel = labels.iat[index,2]
		percent = (i / len(normalized)) * 100;
		print("Label for file " + normalized[i] + ": " + thisLabel + ".  Saving... (Progress: Image " + str(i) + '/' + str(len(normalized)) + ")")
	
		#now we actually copy the files into the correct folder
		if thisLabel == "food":
			copyfile(outPath + normalized[i] + ".jpg", sortedFP + 'food/'+ normalized[i] + ".jpg")
		elif thisLabel == "inside":
			copyfile(outPath + normalized[i] + ".jpg", sortedFP + 'inside/'+ normalized[i] + ".jpg")
		elif thisLabel == "outside":
			copyfile(outPath + normalized[i] + ".jpg", sortedFP + 'outside/'+ normalized[i] + ".jpg")
		elif thisLabel == "drink":
			copyfile(outPath + normalized[i] + ".jpg", sortedFP + 'drink/'+ normalized[i] + ".jpg")
		elif thisLabel == "menu":
			copyfile(outPath + normalized[i] + ".jpg", sortedFP + 'menu/'+ normalized[i] + ".jpg")
	else:
		print("File does not exist in the JSON database")

