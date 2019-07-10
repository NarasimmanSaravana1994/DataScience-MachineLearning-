import pandas as pd
import pickle
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score,precision_recall_fscore_support,roc_curve, auc


############################## Data preparation ##############################
def read_data():
    data = pd.read_csv("D:/Github/Churn_Modelling.csv")
    data = pd.DataFrame(data)
    return data

def data_preparation(data):
    sex = pd.get_dummies(data['Gender'])
    country = pd.get_dummies(data['Geography'])
    data = pd.concat([data,sex,country],axis=1)
    data = data.drop(columns = ['Gender', 'Geography'])
    print(data.columns)
    return data

def prediction_X_columns(dataFrame):
     feature_columns = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard','IsActiveMember', 'EstimatedSalary','Female', 'Male','France', 'Germany', 'Spain']
     return dataFrame[feature_columns]
 
def prediction_Y_columns(dataFrame):
    return dataFrame['Exited']

def standardization(X_train,X_test):
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    return X_train,X_test

def train_test(X,Y):
    from sklearn.model_selection import train_test_split
    return train_test_split(X,Y,test_size=0.3,random_state=100)


############################## SVM Model ##############################
def svm_model(X_train,Y_train,X_test,Y_test):
    from sklearn.svm import SVC    
    svm = SVC(C=1.0,
                kernel='rbf', 
                degree=3,
                gamma='auto_deprecated',
                coef0=0.0,
                shrinking=True,
                probability=False,
                tol=0.001,
                cache_size=200,
                class_weight=None,
                verbose=False,
                max_iter=-1,
                decision_function_shape='ovr',
                random_state=100)

    svm.fit(X_train,Y_train)
    prediction = svm.predict(X_test)
    print("Confusion Matrix:")
    print(confusion_matrix(Y_test,prediction))
    print("Classification Report")
    print(classification_report(Y_test,prediction))
    print("Model Accuracy")
    print(accuracy_score(Y_test,prediction))
    print("Accuracy of SVM Algorithm: {:.2f}%".format(svm.score(X_test,Y_test) * 100))

    return svm

############################## Naive Bayes Model ##############################
def naive_bayes(X_train,Y_train,X_test,Y_test):
    from sklearn.naive_bayes import GaussianNB
    nb = GaussianNB()

    nb.fit(X_train,Y_train)
    prediction = nb.predict(X_test)
    print("Confusion Matrix:")
    print(confusion_matrix(Y_test,prediction))
    print("Classification Report")
    print(classification_report(Y_test,prediction))
    print("Model Accuracy")
    print(accuracy_score(Y_test,prediction))
    print("Accuracy of Naive Bayes: {:.2f}%".format(nb.score(X_test,Y_test) * 100))

    return nb

###################### Random forest Model ##############################
def random_Forest(X_train,Y_train,X_test,Y_test):
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators =1000,
                                criterion='gini',
                                max_depth=None, 
                                min_samples_split=5,
                                min_samples_leaf=5,
                                min_weight_fraction_leaf=0.0,
                                oob_score=True,
                                n_jobs=-1,
                                max_features="auto", 
                                max_leaf_nodes=None,
                                min_impurity_decrease=0.0,
                                min_impurity_split=None,
                                bootstrap=True,
                                verbose=0,
                                warm_start=False,
                                class_weight=None,    
                                random_state = 100)

    rf.fit(X_train,Y_train)
    predictions = rf.predict(X_test)    
    print("Confusion Matrix:")
    print(confusion_matrix(Y_test, predictions))
    print("Classification Report")
    print(classification_report(Y_test, predictions))
    print("Random Forest Algorithm Accuracy Score : {:.2f}%".format(rf.score(X_test,Y_test) * 100))

    pickle.dump(rf, open('randomForestModel.pkl','wb'))

###################### Gradient Boosting Model ##############################
def gradient_boosting(X_train,Y_train,X_test,Y_test):
    from sklearn.ensemble import GradientBoostingClassifier    
    
    gb = GradientBoostingClassifier(n_estimators=1000,
                                   learning_rate = 0.5,
                                   max_features=5,
                                   max_depth = 5,
                                   loss='exponential',
                                   random_state = 100)
    gb.fit(X_train, Y_train)
    predictions = gb.predict(X_test)
    
    print("Confusion Matrix:")
    print(confusion_matrix(Y_test, predictions))
    print("Classification Report")
    print(classification_report(Y_test, predictions))
    
    y_scores_gb = gb.decision_function(X_test)
    fpr_gb, tpr_gb, _ = roc_curve(Y_test, y_scores_gb)
    roc_auc_gb = auc(fpr_gb, tpr_gb)
    print("Gradient Boosting Algorithm Accuracy Score : {:.2f}%".format(gb.score(X_test,Y_test) * 100))
    print("Area under ROC curve = {:0.2f}".format(roc_auc_gb))

###################### XGBoosting Model ##############################
def XG_boosting(X_train,Y_train,X_test,Y_test):
    import xgboost as xgb
    from xgboost.sklearn import XGBClassifier
    
    xgbo = XGBClassifier(n_estimators=1000,
                                   learning_rate = 0.5,
                                   max_features=2,
                                   max_depth = 2,
                                   min_child_weight=1,
                                   gamma=0,
                                   subsample=0.8,
                                   colsample_bytree=0.8,
                                   nthread=4,
                                   scale_pos_weight=1,
                                   seed=27)
    xgbo.fit(X_train, Y_train)
    predictions = xgbo.predict(X_test)
    
    print("Confusion Matrix:")
    print(confusion_matrix(Y_test, predictions))
    print("Classification Report")
    print(classification_report(Y_test, predictions))
    
    print("XGBoosting Algorithm Accuracy Score : {:.2f}%".format(xgbo.score(X_test,Y_test) * 100))

###################### keras Model ##############################
def keras_model(X_train, Y_train):
    import keras
    from keras.models import Sequential
    from keras.layers import Dense

    classifier = Sequential()
    classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu', input_dim = 11))
    classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu'))
    classifier.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))
    classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    classifier.fit(X_train, Y_train, batch_size = 10, nb_epoch = 100)



############################## Cross Validation ##############################
def cross_validation(model,X,Y):
    from sklearn.model_selection import cross_val_score,ShuffleSplit
    cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=100)    
    scores = cross_val_score(model,X,Y,cv=cv)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

###########################################################################
##############  Main function starting here ###############################
if __name__ == "__main__":

    ##############  Data preparation part ###############################

    # Read data
    data = read_data()

    # Data preparation
    dataFrame = data_preparation(data)

    # X column prediction
    X = prediction_X_columns(dataFrame)

    # Y column prediction
    Y = prediction_Y_columns(dataFrame)

    # train and test split
    X_train,X_test,Y_train,Y_test = train_test(X,Y)

    # standardization
    X_train,X_test = standardization(X_train,X_test)

    ##############  Model evaluation part ###############################

    # SVM
    model = svm_model(X_train,Y_train,X_test,Y_test)

    cross_validation(model,X,Y)

    # Naive Bayes
    model = naive_bayes(X_train,Y_train,X_test,Y_test)

    cross_validation(model,X,Y)

    # Random forest

    random_Forest(X_train,Y_train,X_test,Y_test)

    # Gradient Boosting

    gradient_boosting(X_train,Y_train,X_test,Y_test)

    # XGBoosting
    XG_boosting(X_train,Y_train,X_test,Y_test)

    # Keras
    # keras_model(X_train, Y_train)