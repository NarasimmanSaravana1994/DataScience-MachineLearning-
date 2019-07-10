from flask import Flask , jsonify, request, json , render_template
from flask_cors import CORS
from Connector import NaiveBayesTextModel, NaiveScoring
import sqlite3
import pandas as pd
app = Flask(__name__)
#app.debug = True
CORS(app)

@app.route('/Connection/',methods=['POST'])
def Connection():
    Data = json.dumps(request.json)
    Dictionary = json.loads(Data)
    ServerName = Dictionary["Server"]
    ServerIp = Dictionary["ServerIp"]
    UserName = Dictionary["UserName"]
    Password = Dictionary["Password"]
    Database = Dictionary["Database"]
    Port = Dictionary["Port"]
    SId = Dictionary["SId"]
    Query = Dictionary["Query"]
    Independant = Dictionary["Independant"]
    dependant = Dictionary["dependant"]
    Variable = Dictionary["Variable"]
    #Output = NaiveBayesTextModel(ServerName,ServerIp,UserName,Password,Port,Database,SId,Query,Independant,dependant,Variable)
    print("Printed output!!!*****")
    path = 'C:\\Users\mirra.balaji\Music\TextAnalytics\FinalOutput.db'
    SqLiteConnect = sqlite3.connect(path)
    Data = pd.read_sql("select Accuracy,Sensitivity,FalsePositiveRate,Specificity,Mis_Class_Error,F1Score,Thresholds from Performance ", SqLiteConnect)
    print(Data)
    return Data.to_json(orient='records')
    

# def naive(ServerName,ServerIp,UserName,Password,Port,Database,SId,Query,Independant,dependant,Variable):
#     Output = NaiveBayesTextModel(ServerName,ServerIp,UserName,Password,Port,Database,SId,Query,Independant,dependant,Variable)    
#     return "hello"

# @app.route('/training/',methods=['GET'])
# def list():
#     path = 'C:\\Users\mirra.balaji\Music\TextAnalytics\OutputFile.db'
#     SqLiteConnect = sqlite3.connect(path) 
#     Data = pd.read_sql("select * from Data", SqLiteConnect)
#     print(Data)
#     return Data.to_json(orient='table')


@app.route('/Scoring/',methods=['POST'])
def Scoring():
    Data = json.dumps(request.json)
    Dictionary = json.loads(Data)
    ServerName = Dictionary["Server"]
    ServerIp = Dictionary["ServerIp"]
    UserName = Dictionary["UserName"]
    Password = Dictionary["Password"]
    Database = Dictionary["Database"]
    Port = Dictionary["Port"]
    SId = Dictionary["SId"]
    Query = Dictionary["Query"]
    Independant = Dictionary["Independant"]
    dependant = Dictionary["dependant"]
    Variable = Dictionary["Variable"]

    print("SN:"+ServerName+" Sip:"+ ServerIp +" Uid:"+UserName+" Pwd:"+Password+" Db:"+Database+" Port:"+Port+" Sid:"+SId+" query"+Query)
    Output = NaiveScoring(ServerName,ServerIp,UserName,Password,Port,Database,SId,Query,Independant,dependant,Variable)
    print(Output)
    path = 'C:\\Users\mirra.balaji\Music\TextAnalytics\FinalScoring.db'
    SqLiteConnect = sqlite3.connect(path) 
    Data = pd.read_sql("select * from Scoring", SqLiteConnect)
    print(Data)
    return Data.to_json(orient='records')


if __name__ == '__main__':
    app.run(port=8090,threaded=True)

    