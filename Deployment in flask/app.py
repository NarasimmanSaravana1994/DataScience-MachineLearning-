from flask import Flask
from flask import request
import pickle
from sklearn.model_selection import train_test_split

import pandas as pd

app = Flask(__name__)

model = pickle.load(open('randomForestModel.pkl','rb'))
data = pd.read_csv("D:/Github/Churn_Modelling.csv")
data = pd.DataFrame(data)

@app.route('/')
def index():

   dataFrameX = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
   'HasCrCard','IsActiveMember', 'EstimatedSalary']
   X = data[dataFrameX]

   dataFrameY = ['Exited']
   Y = data[dataFrameY]

   X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.3,random_state=100)

   prediction = model.predict([[742.0, 36.0, 2.0, 129748.54, 2.0, 0.0, 0.0, 47271.61,1,0,1,0,1]])
   output = str(prediction[0])
   return output

if __name__ == '__main__':
   app.run(port=5000,debug=True)
