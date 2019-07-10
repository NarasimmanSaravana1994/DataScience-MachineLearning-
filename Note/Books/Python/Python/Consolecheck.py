import pyodbc
import cx_Oracle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score,confusion_matrix,recall_score,precision_score,roc_curve,roc_auc_score
import matplotlib.pyplot as mp
from sklearn.preprocessing import binarize
import sqlite3
import numpy as np
from scipy import stats
from nltk.tokenize import TweetTokenizer
import re
import time
from stop_words import get_stop_words
from nltk import FreqDist
from sklearn.externals import joblib
import warnings
import argparse
import json
import sys

warnings.filterwarnings("ignore")
# Create Connection
def Connector(ServerName,ServerIP,UserID,Password,Database,Port,SId):
    #print("SN:"+ServerName+" Sip:"+ServerIP+" Uid:"+UserID+" Pwd:"+Password+" Db:"+Database+" Port:"+Port+" Sid:"+SId)
    DriverName = ""
    if ServerName != "Oracle":
        if ServerName == "MsSql":
            DriverName = "SQL Server"
        elif ServerName == "MySql":
            DriverName = "MySQL ODBC 5.3 ANSI Driver"
        elif ServerName == "Postgre":
            DriverName = "PostgreSQL ANSI(x64)"
        #print("DriverName: "+DriverName)
        Connection = pyodbc.connect(driver=DriverName,server=ServerIP,uid=UserID,pwd=Password,database=Database)
        return Connection
    else:
        Connection = cx_Oracle.connect(UserID+"/"+Password+"@"+ServerIP+":"+Port+"/"+SId)
        return Connection


# Fetch Input Data
def FetchInputData(Connection,Query):
    Data = pd.read_sql(Query, Connection)
    return Data

# Data Processing Functionalities
def DataProcessing(Data_Comment):

    Tokeniser = TweetTokenizer()

    # Removing HTML Tags
    Data_Comment = Data_Comment.map(lambda Comments: re.sub('<[^<]+?>', '', ''.join(Comments)))

    # Removing Url
    Data_Comment = Data_Comment.map(lambda Comments: re.sub(r"http\S+", "", Comments, flags=re.MULTILINE))

    # Tokenise
    Data_Comment = Data_Comment.map(lambda Comments: Tokeniser.tokenize(Comments))

    # Stop Words Removal
    stop_words = get_stop_words('english')
    Data_Comment = Data_Comment.map(lambda Comments: [elem for elem in Comments if elem.lower() not in stop_words])

    # Symbol removal
    Data_Comment = Data_Comment.map(lambda Comments: [re.sub(r'([^\sA-Za-z]|_)+', '', elem) for elem in Comments])

    ## Joining Words back to Sentences
    Data_Comment = Data_Comment.map(lambda Comments: ' '.join(Comments))

    return Data_Comment


# Naive Bayes Classifier
def NaiveBayes(ProcessedData,Data_Category):
    # sqlite connection
    path = 'C:\\Users\mirra.balaji\Music\FinalOutput.db'
    SqLiteConnect = sqlite3.connect(path)
    SqLiteCursor = SqLiteConnect.cursor()

    PostiveBag = ""
    NegativeBag = ""

    for i in range(0, len(ProcessedData)):
        if Data_Category[i] == 0:
            NegativeBag = NegativeBag + ' ' + ProcessedData[i]
        else:
            PostiveBag = PostiveBag + ' ' + ProcessedData[i]

    tokenizer = TweetTokenizer()
    PostiveBag = tokenizer.tokenize(PostiveBag)
    NegativeBag = tokenizer.tokenize(NegativeBag)

    # FreqDistribution of Neg
    PositiveFrequency = FreqDist(PostiveBag)
    NegativeFrequency = FreqDist(NegativeBag)

    NegativeFrequency = NegativeFrequency.most_common(len(NegativeFrequency))
    PositiveFrequency = PositiveFrequency.most_common(len(PositiveFrequency))

    SqLiteCursor.execute("DROP TABLE IF EXISTS WordFrequency")
    SqLiteCursor.execute("CREATE TABLE WordFrequency(Word, Frequency, Category)")

    SqLiteCursor.executemany("INSERT INTO WordFrequency VALUES(?,?,'Positive')", PositiveFrequency)
    SqLiteCursor.executemany("INSERT INTO WordFrequency VALUES(?,?,'Negative')", NegativeFrequency)


    TDIDF = TfidfVectorizer(min_df=1, stop_words='english')

    CommentTrain, CommentTest, CategTrain, CategTest = train_test_split(ProcessedData, Data_Category, test_size=0.3, random_state=1)
    NaiveBayesObject = MultinomialNB()

    CommentTrain_TDIDF = TDIDF.fit_transform(CommentTrain)

    CategTrain = CategTrain.astype('int')
    NaiveBayesObject.fit(CommentTrain_TDIDF, CategTrain)

    CommentTest_TDIDF = TDIDF.transform(CommentTest)
    CategTest = CategTest.astype('int')
    PredictClass = NaiveBayesObject.predict(CommentTest_TDIDF)

    probability_0 = NaiveBayesObject.predict_proba(CommentTest_TDIDF)[:, 0]
    probability_1 = NaiveBayesObject.predict_proba(CommentTest_TDIDF)[:, 1]

    joblib.dump(NaiveBayesObject,'Model.pkl')
    joblib.dump(TDIDF,'vector.pkl')
    SqLiteCursor.execute("DROP TABLE IF EXISTS Data")
    SqLiteCursor.execute("DROP TABLE IF EXISTS Reviews")
    SqLiteCursor.execute(
        "CREATE TABLE Data (Comment_Index int,Comments text, Actual int,Probability_0 int,Probability_1 int, Predicted int)") #str(round(thresholds, 4))
    for count in range(0, len(CommentTest)):
        SqLiteCursor.execute("INSERT INTO Data VALUES (?,?,?,?,?,?)", (
        int(CommentTest.index[count]), CommentTest.values[count], int(CategTest.values[count]), str(round(probability_0[count],4)),
        probability_1[count], int(PredictClass[count])))



    SqLiteCursor.execute("DROP TABLE IF EXISTS ConfusionTable")
    SqLiteCursor.execute('''CREATE TABLE ConfusionTable (Thresholds float,TrueNegative int, FalsePositive int,FalseNegative int,TruePositive int,Sensitivity float,
    Specificity float,FalsePositiveRate float,Accuracy float,Mis_Clas_Error float,F1Score float,Precision float)''')

    for thresholds in np.arange(0.0125, 1.0125, 0.0125):
        NewPredictClass = binarize(probability_1, thresholds)[0]
        confusion = confusion_matrix(CategTest, NewPredictClass)
        TP = confusion[1, 1]
        FN = confusion[1, 0]
        FP = confusion[0, 1]
        TN = confusion[0, 0]
        Sensitivity = TP / float(TP + FN)
        Specificity = TN / float(TN + FP)
        False_Positive_rate = FP / float(TN + FP)
        Accuracy = (TP + TN) / float(TN + TP + FN + FP)
        MisClassificationError = (FP + FN) / float(TP + TN + FP + FN)
        Precision = TP / float(TP + FP)
        F1Score = 2 * (Sensitivity * Precision) / (Sensitivity + Precision)
        SqLiteCursor.execute("INSERT INTO ConfusionTable VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
        str(round(thresholds, 4)), int(TN), int(FP), int(FN), int(TP), str(round(Sensitivity,3)), str(round(Specificity,3)), str(round(False_Positive_rate,3)),
        str(round(Accuracy,3)), str(round(MisClassificationError,3)), round(F1Score,3), str(round(Precision,3))))

    SqLiteConnect.execute("DROP TABLE IF EXISTS Performance")
    SqLiteConnect.execute('''CREATE TABLE Performance (Thresholds float, TrueNegative int, FalsePositive int, FalseNegative int, TruePositive int, Sensitivity float,
    Specificity float, FalsePositiveRate float, Accuracy float, Mis_Class_Error float, F1Score float,Precision float)''')
    SqLiteConnect.execute("insert into Performance select * from ConfusionTable where F1Score=(select max(F1Score) from ConfusionTable)")

    SqLiteConnect.commit()
    return True

# Main Execution Method
def NaiveBayesTextModel(argv):
    temp={}
    try:
        
        parser = argparse.ArgumentParser(description='json load and print')
        parser.add_argument('-i','--inputstring', help='Input String in JSON format',required=True)
        args = parser.parse_args()
        inp = args.inputstring
        contents = inp[1:-1]
        temp = dict(item.split(":") for item in contents.split(","))
        ServerName = temp["ServerName"]
        ServerIP = temp["ServerIP"]
        UserID = temp["UserID"]
        Password= temp["Password"]
        Database= temp["Database"]
        Port= temp["Port"]
        SId= temp["SId"]
        Query= temp["Query"]
        InDependantVariable= temp["InDependantVariable"]
        DependantVariable= temp["DependantVariable"]
        Variable= temp["Variable"]
        #print(ServerName, ServerIP, UserID, Password, Database, Port, SId)
        Connection = Connector(ServerName, ServerIP, UserID, Password, Database, Port, SId)
        Data = FetchInputData(Connection, Query)

        Data_Comment = Data[InDependantVariable]
        Data_Category = Data[DependantVariable]

        OtherCateg = None

        for categ in set(Data_Category):
            if categ != Variable:
                OtherCateg = categ

        Data.loc[Data[DependantVariable] == Variable, DependantVariable] = 1
        Data.loc[Data[DependantVariable] == OtherCateg, DependantVariable] = 0
        #print(set(Data_Category))
        ProcessedData = DataProcessing(Data_Comment)
        #print("Call NaiveBayes")
        Output = NaiveBayes(ProcessedData,Data_Category)
        print("Output recevied")
        
    except Exception as e:
      return e
      sys.exit(2)




if __name__ == "__main__":
   NaiveBayesTextModel(sys.argv[:])


