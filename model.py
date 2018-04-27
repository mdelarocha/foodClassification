# Notebook to make model, originally ran on Databricks
# Import libraries

from sparkdl import readImages
from pyspark.sql.functions import lit 

# make the images dataframes

path = "/CS4301/normalize/"

food_df = readImages(path + "food").withColumn("label", lit(0))
inside_df = readImages(path + "inside").withColumn("label", lit(1))
outside_df = readImages(path + "outside").withColumn("label", lit(2))
menu_df = readImages(path + "menu").withColumn("label", lit(3))
drink_df = readImages(path + "drink").withColumn("label", lit(4))

# Make the training and testing dataset

f_train, f_test = food_df.randomSplit([0.8, 0.2])
i_train, i_test = inside_df.randomSplit([0.8, 0.2])
o_train, o_test = outside_df.randomSplit([0.8, 0.2])
m_train, m_test = menu_df.randomSplit([0.8, 0.2])
d_train, d_test = drink_df.randomSplit([0.8, 0.2])

# Union the datasets 
# Function used to union several dataframes 

from pyspark.sql import DataFrame

def unionAll(*dfs):
    return reduce(DataFrame.unionAll, dfs)

# Training and Testing dataframes

training_df = unionAll(f_train, i_train, o_train, m_train, d_train)
testing_df = unionAll(f_test, i_test, o_test, m_test, d_test)

# Make the model using spark deep learning functions 
# Functions utilized based on the Databricks Deep Learning Documentation 

from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from sparkdl import DeepImageFeaturizer 

featurizer = DeepImageFeaturizer(inputCol="image", outputCol="features", modelName="InceptionV3")
lr = LogisticRegression(maxIter=20, regParam=0.05, elasticNetParam=0.3, labelCol="label")
p = Pipeline(stages=[featurizer, lr])
p_model = p.fit(training_df)

# Test the predictions on the testing dataframe

predictions = p_model.transform(testing_df)

predictions.select("filepath", "prediction").show(truncate=False)

# Evaluator function to validate our accuracy, using PySpark ML evaluations 
# Code based on Databricks documentation and functions

from pyspark.ml.evaluation import MulticlassClassificationEvaluator

df = p_model.transform(testing_df)
df.show()

predictAndLabel = df.select("prediction", "label")
evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
print("Training set accuracy = " + str(evaluator.evaluate(predictAndLabel)))
