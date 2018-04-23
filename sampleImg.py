# Simple Script to sample from Dataset

import os 
import shutil 
import random 
from shutil import copyfile

sourcedir = 'Filestore/tables/yelp_photos'
newdir  = 'Filestore/tables/photosSample

filenames = random.sample(os.listdir(sourcedir), 3500)

for i in filenames:
    shutil.copy2(sourcedir + i, newdir)
