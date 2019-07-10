import pyodbc, sklearn
import pandas as pd
import nltk
import matplotlib.pyplot as plt
import warnings
import numpy as np
warnings.filterwarnings("ignore", category=DeprecationWarning)
import re
from nltk.tokenize import TweetTokenizer
import time

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report,recall_score
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

## Setting Pandas PD options
pd.options.mode.chained_assignment = None


cList = {"ain't": "am not","aren't": "are not","can't": "cannot","can't've": "cannot have","'cause": "because","could've": "could have","couldn't": "could not","couldn't've": "could not have","didn't": "did not","doesn't": "does not","don't": "do not","hadn't": "had not","hadn't've": "had not have","hasn't": "has not","haven't": "have not","he'd": "he would","he'd've": "he would have",
         "he'll": "he will","he'll've": "he will have","he's": "he is","how'd": "how did","how'd'y": "how do you","how'll": "how will","how's": "how is","I'd": "I would","I'd've": "I would have","I'll": "I will","I'll've": "I will have","I'm": "I am","I've": "I have","isn't": "is not","it'd": "it had","it'd've": "it would have",
         "it'll": "it will","it'll've": "it will have","it's": "it is","let's": "let us","ma'am": "madam","mayn't": "may not","might've": "might have","mightn't": "might not","mightn't've": "might not have","must've": "must have","mustn't": "must not","mustn't've": "must not have","needn't": "need not","needn't've": "need not have","o'clock": "of the clock","oughtn't": "ought not",
         "oughtn't've": "ought not have","shan't": "shall not","sha'n't": "shall not","shan't've": "shall not have","she'd": "she would","she'd've": "she would have","she'll": "she will","she'll've": "she will have","she's": "she is","should've": "should have",
         "shouldn't": "should not","shouldn't've": "should not have","so've": "so have","so's": "so is","that'd": "that would","that'd've": "that would have","that's": "that is","there'd": "there had","there'd've": "there would have","there's": "there is","they'd": "they would","they'd've": "they would have","they'll": "they will","they'll've": "they will have","they're": "they are",
         "they've": "they have","to've": "to have","wasn't": "was not","we'd": "we had","we'd've": "we would have","we'll": "we will","we'll've": "we will have","we're": "we are","we've": "we have","weren't": "were not","what'll": "what will","what'll've": "what will have","what're": "what are","what's": "what is","what've": "what have",
         "when's": "when is","when've": "when have","where'd": "where did","where's": "where is","where've": "where have","who'll": "who will","who'll've": "who will have","who's": "who is","who've": "who have","why's": "why is","why've": "why have","will've": "will have","won't": "will not","won't've": "will not have","would've": "would have","wouldn't": "would not",
         "wouldn't've": "would not have","y'all": "you all","y'alls": "you alls","y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have","you'd": "you had","you'd've": "you would have","you'll": "you you will","you'll've": "you you will have","you're": "you are","you've": "you have"}

c_re = re.compile('(%s)' % '|'.join(cList.keys()))

def expandContractions(text, c_r=c_re):
    def replace(match):
        return cList[match.group(0)]
    return c_r.sub(replace, text)


## Connecting to DataBas5e
conn = pyodbc.connect("DRIVER={SQL Server Native Client 11.0};SERVER=bellsqlnew;UID=qa;PWD=bellqa;DATABASE=NORTHWIND")
cur = conn.cursor()

##ReadData
df = pd.read_sql("select * from MovieComments", conn)

df.loc[df["Category"] == 'neg',"Category"]=0
df.loc[df["Category"] == 'pos',"Category"]=1

##
##df_Comment = df["Comments"]
##df_Categ = df["Category"]
##
##
##import time
##
##from nltk.tokenize import TweetTokenizer
##
##tokenizer=TweetTokenizer()
##
##
#### Expanding Contractions
####expanded_df_comment=[expandContractions(df_Comment[i].lower()) for i in range(0,len(df_Comment))]
##
##
#### Removing HTML Tags
##df_Comment = df_Comment.map(lambda Comments: re.sub('<[^<]+?>', '', ' '.join(Comments)))
##
##
##url_removal=[re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''','',regularized[k]) for k in range(0,len(regularized))]
##
##sym_removal=[re.sub(r'([^\s\w]|_)+','', url_removal[l]) for l in range(0,len(url_removal))]
##
##tokens=[tokenizer.tokenize(sym_removal[m]) for m in range(0,len(sym_removal))]
##
##test=[]
##
##stop_words = set(stopwords.words("english"))
##stop_words.remove('not')
##stop_words.update(('br','nt','movie','film','even'))
###filtered = [for n in range(0,len(tokens)) for o in tokens[n] if o not in stop_words if o==len(tokens[n])]
###
###
##filtered=[]
##for n in range(0,len(tokens)):
##    test=[]
##    for o in range(0,len(tokens[n])):
##        if tokens[n][o] not in stop_words:
##            test.append(tokens[n][o])
##    filtered.append(test)
##
##for p in range(0, len(filtered)):
##    df_Comment[p]=' '.join(filtered[p])
##
##
##cv = CountVectorizer(min_df=1,ngram_range=(1,2))
##x_train, x_test, y_train, y_test = train_test_split(df_Comment, df_Categ, test_size=0.2, random_state=4)
##
##Comment_tr = cv.fit_transform(x_train)
##
###print(set(cv.get_feature_names()))
##
##
##mnb= MultinomialNB()
##
##
##y_train=y_train.astype('int')
##mnb.fit(Comment_tr,y_train)
##Comment_tst=cv.transform(x_test)
##y_test=y_test.astype('int')
### #
### # # Metrics
##print(accuracy_score(y_test, mnb.predict(Comment_tst))*100)
##
##print(time.clock()-start)





