import pyodbc, sklearn
import pandas as pd
import nltk
import matplotlib.pyplot as plt
import warnings
import numpy as np
warnings.filterwarnings("ignore", category=DeprecationWarning)
import re

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


## Connecting to DataBase
conn = pyodbc.connect("DRIVER={SQL Server Native Client 11.0};SERVER=bellsqlnew;UID=qa;PWD=bellqa;DATABASE=NORTHWIND")
cur = conn.cursor()

##ReadData
df = pd.read_sql("select Top 10000 * from SampleComments", conn)





df.loc[df["Category"]=='neg',"Category"]=0
df.loc[df["Category"]=='pos',"Category"]=1

df_Comment = df["Comments"]
df_Categ = df["Category"]






#PreProcessing



for comment in range(0,len(df_Comment)):
    print(comment)

    ##Expanding Contractions
    expanded_words=expandContractions(df_Comment[comment])



    ##Removing Urls
    url_removal=re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''','',expanded_words)


    ## Removing Html Tags
    regular_exp=re.compile(r'<.*?>')
    regularized=regular_exp.sub('',url_removal)



    ##Tokenize
    tokens=nltk.word_tokenize(regularized)


    #Removing Symbols
    symbols_removal=[]
    for word in tokens:
        symbols="\`~!@#$%^&*()_-+=|}]{[\"':;?/>.<,"
        for i in range(0, len(symbols)):
            word = word.replace(symbols[ i ], "")
        if len(word) > 0:
            if not word.isdigit():
                symbols_removal.append(word.lower())

    # StopWords
    stop_words = set(stopwords.words("english"))
    stop_words.remove('not')
    stop_words.update(('br','nt','movie','film','even'))
    filtered = [ w for w in symbols_removal if not w in stop_words ]


    #Lemmatization
    lemmatizer=WordNetLemmatizer()
    lemmatized_words=[lemmatizer.lemmatize(wd,pos="v") for wd in filtered]

    ##Assignment
    df_Comment[comment]=' '.join(lemmatized_words)




## Training The Model

cv = CountVectorizer(min_df=1,stop_words='english')
x_train, x_test, y_train, y_test = train_test_split(df_Comment, df_Categ, test_size=0.2, random_state=4)

Comment_tr = cv.fit_transform(x_train)

#print(set(cv.get_feature_names()))



mnb= MultinomialNB()



y_train=y_train.astype('int')
mnb.fit(Comment_tr,y_train)
Comment_tst=cv.transform(x_test)
y_test=y_test.astype('int')
# #
# # # Metrics
print(accuracy_score(y_test, mnb.predict(Comment_tst)))


#
# print(confusion_matrix(y_test, mnb.predict(Comment_tst)))
# print(classification_report(y_test,mnb.predict(Comment_tst)))
# print(recall_score(y_test,mnb.predict(Comment_tst)))



## Frequency Ditribution
# x_train_array=np.array(x_train)
#
#
# word_cloud=[]
# for i in range(0,len(x_train_array)):
#     tokens=nltk.word_tokenize(x_train_array[i])
#     word_cloud=word_cloud+tokens
#
# freq_dist = nltk.FreqDist(word_cloud)
#
# freq_dist_list=freq_dist.most_common(10)
#
#
#
#
# n_groups = len(freq_dist_list)
#
# vals_films = [x[1] for x in freq_dist_list]
# legends_films = [x[0] for x in freq_dist_list]
#
# fig, ax = plt.subplots()
#
# index = np.arange(n_groups)
# bar_width = 0.25
#
# opacity = 0.4
#
# rects1 = plt.bar(index, vals_films, bar_width,
#                  alpha=opacity,
#                  color='b',
#                  label='Ocurrences')
#
#
# plt.xlabel('Occurrences')
# plt.ylabel('Words')
# plt.title('Occurrences by word')
# plt.xticks(index + bar_width, legends_films)
# plt.legend()
#
# plt.tight_layout()
# plt.show()
#
# plt.imshow(word_cloud)
# plt.axis('off')
# plt.show()
#
#
#
#
# # Creating DataFrame
# # list2=[]
# # y_test_array=np.array(y_test)
# # x_test_array=np.array(x_test)
# #
# #
# # predicted=mnb.predict(Comment_tst)
# # for i in range(0,len(y_test_array)):
# #     list1=[x_test.index[i],x_test_array[i],y_test_array[i],predicted[i]]
# #     list2.append(list1)
# #
# #
# #
# # columns=['Index','Test_Comments','Actual','Predicted']
# # index=range(0,len(y_test))
# # data_frame=pd.DataFrame(list2,columns=columns, index=index)
# # print(data_frame)
#
#
# #

#
# conn.close()


