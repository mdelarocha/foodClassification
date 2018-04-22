#Preprocess

# Import libraries needed 

from sparkdl import readImages
from pyspark.sql.functions import lit
from pyspark.sql import SQLContext
from pyspark.sql.functions import col
from pyspark.sql.types import StructType,StructField, LongType

# Find distinct labels

df=spark.read.json("/FileStore/tables/photos.json", multiLine=False)
df.groupBy("label").count().show()
df.select("label").distinct().count()
df.select("label").distinct().show()

# Image dataframe

img_dir='/FileStore/tables/yelp_photos'
images_df=readImages(img_dir)

# Wait until we map and normalize the images
# images_train, images_test=images_df.randomSplit([0.7,0.3]) 
