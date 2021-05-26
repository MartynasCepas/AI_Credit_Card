import h2o
import matplotlib.pyplot as plt

h2o.init()

h2o.ls()

df = h2o.import_file("./data/data.csv")
colmeans = df.mean()

print(colmeans)

# generate a random vector for splitting
r = df[0].runif()

# split out 60% for training
train = df[ r < 0.6 ]

# split out 30% for validation
valid = df[ (0.6 <= r) & (r < 0.9) ]

# split out 10% for testing
test = df[ 0.9 <= r ]

# import the glm estimator and train the model
from h2o.estimators.glm import H2OGeneralizedLinearEstimator

my_model = H2OGeneralizedLinearEstimator(family="gaussian")
my_model.train(x=df.names, y="default payment next month", training_frame=df)

# print the GLM coefficients, can also perform my_model.coef_norm() to get the normalized coefficients
my_model.coef()

# get the null deviance from the training set metrics
my_model.null_deviance()

# get the residual deviance from the training set metrics
my_model.residual_deviance()

# get the null deviance from the validation set metrics (similar for residual deviance)
#my_model.null_deviance(valid=True)

# now generate a new metrics object for the test hold-out data:
# create the new test set metrics
my_metrics = my_model.model_performance(test_data=test)
print("performance: ", my_metrics)
# returns the test null dof
my_metrics.null_degrees_of_freedom()

# returns the test res. deviance
my_metrics.residual_deviance()

# returns the test aic
my_metrics.aic()

preds = my_model.predict(test)
print(preds)