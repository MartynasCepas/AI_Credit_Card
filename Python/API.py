from flask import Flask
from flask_restful import Resource, Api, reqparse
import h2o
import pandas as pd

app = Flask(__name__)
api = Api(app)

h2o.init()

## load saved model
model_path = './Python/models/DeepLearning_model_FINAL'
uploaded_model = h2o.load_model(model_path)

# argument parsing
parser = reqparse.RequestParser(bundle_errors=True) #if there are 2 errors, both's msg will be printed
parser.add_argument('LIMIT_BAL')
parser.add_argument('EDUCATION')
parser.add_argument('AGE')
parser.add_argument('PAY_MEAN')
parser.add_argument('PAY_AMT_MEAN')
parser.add_argument('PAY_DIFF')

#Categorical Columns - enum
#Numerical Columns - real
col_dict = {'LIMIT_BAL' : 'real',
            'EDUCATION' : 'real',
            'AGE' : 'real',
            'PAY_MEAN': 'real',
            'PAY_AMT_MEAN':'real',
            'PAY_DIFF':'real'}

#prepare empty test data frame to be fed to the model
data = {}

# results dict
item_dict = {}


class CreditPredict(Resource):
    def get(self):
        args = parser.parse_args()
        limit_bal = int(args['LIMIT_BAL'])
        education = int(args['EDUCATION'])
        age = int(args['AGE'])
        pay_mean = float(args['PAY_MEAN'])
        pay_amt_mean = float(args['PAY_AMT_MEAN'])
        pay_diff = float(args['PAY_DIFF'])

        application_outcome = 'declined'

        # put key:value pairs in empty dict called data
        data['LIMIT_BAL'] = limit_bal
        data['EDUCATION'] = education
        data['AGE'] = age
        data['PAY_MEAN'] = pay_mean
        data['PAY_AMT_MEAN'] = pay_amt_mean
        data['PAY_DIFF'] = pay_diff

        data['application_outcome'] = application_outcome

        # creating dataframe from dict
        testing = pd.DataFrame(data, index=[0])

        # converting pandas to h2o dataframe
        test = h2o.H2OFrame(testing, column_types=col_dict)

        # making predictions
        pred_ans = uploaded_model.predict(test).as_data_frame()

        # put key:value pairs in empty dict called item_dict
        item_dict['Prediction'] = pred_ans.predict.values[0]
        item_dict['default payment next month'] = 0 if pred_ans.predict.values[0] < 0.5 else 1

        return {'ans': item_dict}

api.add_resource(CreditPredict, '/')

app.run(debug=True, port= 1234)