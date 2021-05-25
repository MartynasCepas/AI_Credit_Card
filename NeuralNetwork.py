import h2o
from h2o.estimators import H2ODeepLearningEstimator
h2o.init(nthreads = -1)

# Import the insurance dataset into H2O:
credit = h2o.import_file("./data/data.csv")

r = credit[0].runif()

# split out 60% for training
train = credit[ r < 0.6 ]

# split out 30% for validation
valid = credit[ (0.6 <= r) & (r < 0.9) ]

# split out 10% for testing
test = credit[ 0.9 <= r ]

predictors = ["LIMIT_BAL", "EDUCATION", "AGE"]
response = "default payment next month"
ignored = ["ID"]

# Build and train the model:
dl = H2ODeepLearningEstimator(distribution="tweedie",
                               hidden=[1],
                          #     ignored_columns = ignored,
                               epochs=1000,
                               adaptive_rate=True,
                               train_samples_per_iteration=-1,
                               reproducible=False,
                               activation="Tanh",
                               single_node_mode=False,
                               balance_classes=False,
                               force_load_balance=True,
                               tweedie_power=1.5,
                               score_training_samples=0,
                               score_validation_samples=0,
                               stopping_rounds=0,
                               loss="automatic",
                              # rate=0.001,
                               standardize=True)
dl.train(x=predictors, y=response, training_frame=train, validation_frame=valid)

# Eval performance:
perf = dl.model_performance()
# Generate predictions on a test set (if necessary):
pred = dl.predict(test)

my_local_model = h2o.download_model(dl, path="./models/")