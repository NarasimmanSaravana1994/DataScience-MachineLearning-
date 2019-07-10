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
import warnings
from nltk import FreqDist
warnings.filterwarnings("ignore",category=DeprecationWarning)

class NaiveBayes:

    def Connector(Self,ServerName, ServerIP, UserID, Password, Database, Port, SId):
        DriverName = None
        if ServerName is not "Oracle":
            if ServerName is "MsSql":
                DriverName = "SQL Server Native Client 11.0"
            elif ServerName is "MySql":
                DriverName = "MySQL ODBC 5.3 ANSI Driver"
            elif ServerName is "Postgre":
                DriverName = "PostgreSQL ANSI(x64)"
            Connection = pyodbc.connect(driver=DriverName, server=ServerIP, uid=UserID, pwd=Password, database=Database)
            return Connection
        else:
            Connection = cx_Oracle.connect(UserID + "/" + Password + "@" + ServerIP + ":" + Port + "/" + SId)
            return Connection

    # Fetch Input Data
    def FetchInputData(Self,Connection, Query):
        Data = pd.read_sql(Query, Connection)
        return Data

    # Data Processing Functionalities
    def DataProcessing(Self,Data_Comment):
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
    def NaiveBayes(Self,ProcessedData, Data_Category):
        # sqlite connection
        path = 'C:\\Users\mirra.balaji\Music\TextAnalytics\SampleOutputFile.db'
        SqLiteConnect = sqlite3.connect(path)
        SqLiteCursor = SqLiteConnect.cursor()

        TDIDF = TfidfVectorizer(min_df=1, stop_words='english')

        CommentTrain, CommentTest, CategTrain, CategTest = train_test_split(ProcessedData, Data_Category, test_size=0.3,
                                                                            random_state=1)
        NaiveBayesObject = MultinomialNB()

        CommentTrain_TDIDF = TDIDF.fit_transform(CommentTrain)

        CategTrain = CategTrain.astype('int')
        NaiveBayesObject.fit(CommentTrain_TDIDF, CategTrain)

        CommentTest_TDIDF = TDIDF.transform(CommentTest)
        CategTest = CategTest.astype('int')
        PredictClass = NaiveBayesObject.predict(CommentTest_TDIDF)

        probability_0 = NaiveBayesObject.predict_proba(CommentTest_TDIDF)[:, 0]
        probability_1 = NaiveBayesObject.predict_proba(CommentTest_TDIDF)[:, 1]

        SqLiteCursor.execute("DROP TABLE IF EXISTS Data")
        SqLiteCursor.execute("DROP TABLE IF EXISTS Reviews")
        SqLiteCursor.execute(
            "CREATE TABLE Data (Comment_Index int,Comments text, Actual int,Probability_0 int,Probability_1 int, Predicted int)")
        for count in range(0, len(CommentTest)):
            SqLiteCursor.execute("INSERT INTO Data VALUES (?,?,?,?,?,?)", (
                int(CommentTest.index[count]), CommentTest.values[count], int(CategTest.values[count]),
                probability_0[count],
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
                str(round(thresholds, 4)), int(TN), int(FP), int(FN), int(TP), Sensitivity, Specificity,
                False_Positive_rate,
                Accuracy, MisClassificationError, F1Score, Precision))

        SqLiteConnect.commit()
        return True

    # Main Execution Method
    def NaiveBayesTextModel(Self,ServerName, ServerIP, UserID, Password, Database, Port, SId, Query, InDependantVariable,
                            DependantVariable, Variable):
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
        print(set(Data_Category))
        ProcessedData = DataProcessing(Data_Comment)

        Output = NaiveBayes(ProcessedData, Data_Category)
        return Output