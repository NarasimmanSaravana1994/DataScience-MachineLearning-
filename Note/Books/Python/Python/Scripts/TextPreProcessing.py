import time
import pyodbc, sklearn
import pandas as pd
import nltk
import matplotlib.pyplot as plt
import warnings
import numpy as np
warnings.filterwarnings("ignore", category=DeprecationWarning)
import re
import time
import sqlite3

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report,recall_score
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer

import DBConnection



## Variable Declaration
tokenizer=TweetTokenizer()

cList = {"ain't": "am not","Ain't": "am not","aren't": "are not","Aren't": "are not","can't": "cannot","Can't": "cannot","can't've": "cannot have","Can't've": "cannot have","'cause": "because","could've": "could have","Could've": "could have","couldn't": "could not","Couldn't": "could not","couldn't've": "could not have","Couldn't've": "could not have","didn't": "did not","Didn't": "did not","doesn't": "does not","Doesn't": "does not","don't": "do not","Don't": "do not","hadn't": "had not","Hadn't": "had not","hadn't've": "had not have","Hadn't've": "had not have","hasn't": "has not","Hasn't": "has not","haven't": "have not","Haven't": "have not","he'd": "he would","He'd": "he would","he'd've": "he would have",
         "He'd've": "he would have","he'll": "he will","He'll": "he will","he'll've": "he will have","He'll've": "he will have","he's": "he is","He's": "he is","how'd": "how did","How'd": "how did","how'd'y": "how do you","How'd'y": "how do you","how'll": "how will","How'll": "how will","how's": "how is","How's": "how is","I'd": "i would","i'd": "i would","I'd've": "I would have","i'd've": "i would have","I'll": "I will","i'll": "i will","I'll've": "I will have","i'll've": "i will have","I'm": "I am","i'm": "i am","I've": "I have","i've": "i have","isn't": "is not","Isn't": "is not","it'd": "it had","It'd": "it had","it'd've": "it would have","It'd've": "it would have",
         "it'll": "it will","It'll": "it will","it'll've": "it will have","It'll've": "it will have","it's": "it is","It's": "it is","let's": "let us","Let's": "let us","ma'am": "madam","Ma'am": "madam","mayn't": "may not","Mayn't": "may not","might've": "might have","Might've": "might have","mightn't": "might not","Mightn't": "might not","mightn't've": "might not have","Mightn't've": "might not have","must've": "must have","Must've": "must have","mustn't": "must not","Mustn't": "must not","mustn't've": "must not have","Mustn't've": "must not have","needn't": "need not","Needn't": "need not","needn't've": "need not have","Needn't've": "need not have","o'clock": "of the clock","O'clock": "of the clock","oughtn't": "ought not",
         "Oughtn't": "ought not","oughtn't've": "ought not have","Oughtn't've": "ought not have","shan't": "shall not","Shan't": "shall not","sha'n't": "shall not","Sha'n't": "shall not","shan't've": "shall not have","Shan't've": "shall not have","she'd": "she would","She'd": "she would","she'd've": "she would have","She'd've": "she would have","she'll": "she will","She'll": "she will","she'll've": "she will have","She'll've": "she will have","she's": "she is","She's": "she is","should've": "should have","Should've": "should have",
         "shouldn't": "should not","Shouldn't": "should not","shouldn't've": "should not have","Shouldn't've": "should not have","so've": "so have","So've": "so have","so's": "so is","So's": "so is","that'd": "that would","That'd": "that would","that'd've": "that would have","That'd've": "that would have","that's": "that is","That's": "that is","there'd": "there had","There'd": "there had","there'd've": "there would have","There'd've": "there would have","there's": "there is","There's": "there is","they'd": "they would","They'd": "they would","they'd've": "they would have","They'd've": "they would have","they'll": "they will","They'll": "they will","they'll've": "they will have","They'll've": "they will have","they're": "they are",
         "They're": "they are","they've": "they have","They've": "they have","to've": "to have","To've": "to have","wasn't": "was not","Wasn't": "was not","we'd": "we had","We'd": "we had","we'd've": "we would have","We'd've": "we would have","we'll": "we will","We'll": "we will","we'll've": "we will have","We'll've": "we will have","we're": "we are","We're": "we are","we've": "we have","We've": "we have","weren't": "were not","Weren't": "were not","what'll": "what will","What'll": "what will","what'll've": "what will have","What'll've": "what will have","what're": "what are","What're": "what are","what's": "what is","What's": "what is","what've": "what have","What've": "what have",
         "when's": "when is","When's": "when is","when've": "when have","When've": "when have","where'd": "where did","Where'd": "where did","where's": "where is","Where's": "where is","where've": "where have","Where've": "where have","who'll": "who will","Who'll": "who will","who'll've": "who will have","Who'll've": "who will have","who's": "who is","Who's": "who is","who've": "who have","Who've": "who have","why's": "why is","Why's": "why is","why've": "why have","Why've": "why have","will've": "will have","Will've": "will have","won't": "will not","Won't": "will not","won't've": "will not have","Won't've": "will not have","would've": "would have","Would've": "would have","wouldn't": "would not","Wouldn't": "would not",
         "wouldn't've": "would not have","Wouldn't've": "would not have","y'all": "you all","Y'all": "you all","y'alls": "you alls","Y'alls": "you alls","y'all'd": "you all would","Y'all'd": "you all would","y'all'd've": "you all would have","Y'all'd've": "you all would have","y'all're": "you all are","Y'all're": "you all are","y'all've": "you all have","Y'all've": "you all have","you'd": "you had","You'd": "you had","you'd've": "you would have","You'd've": "you would have","you'll": "you you will","You'll": "you you will","you'll've": "you you will have","You'll've": "you you will have","you're": "you are","You're": "you are","you've": "you have","You've": "you have"}

c_re = re.compile('(%s)' % '|'.join(cList.keys()))

pd.options.mode.chained_assignment = None

start=time.clock()

filtered=[]

##Fucntion Calls

def expandContractions(text, c_r=c_re):
    def replace(match):
        return cList[match.group(0)]
    return c_r.sub(replace, text)


def preProcessing():

    df_Comment, df_Category = DBConnection.dbConnection()


    #Contractions Expander
    expanded_df_comment=[expandContractions(df_Comment[i]) for i in range(0,len(df_Comment))]


    #HTML Tags Remover
    regular_exp = re.compile(r'<.*?>')
    regularized=[regular_exp.sub('',expanded_df_comment[j])for j in range(0,len(expanded_df_comment))]



    #Url Remover
    url_removal=[re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''','',regularized[k]) for k in range(0,len(regularized))]

    #Symbol Remover
    sym_removal=[re.sub(r'([^\sa-zA-Z]|_)+','', url_removal[l]) for l in range(0,len(url_removal))]

    #WordContractions
    contract_free=[' '.join(re.findall('[A-Z][^a-z]*[^A-Z]*',sym_removal[temp]))for temp in range(0,len(sym_removal))]


    #Tokenizer
    tokens=[tokenizer.tokenize(contract_free[m]) for m in range(0,len(contract_free))]

    #StopWords Remover
    stop_words = set(stopwords.words("english"))
    #stop_words.remove('not')
    stop_words.update(('br','nt','movie','film','even','With','If','This','I','Their','To','From','That','Whom','Once','Who','Me','What','Having','They',
                       'Ours','Been','Yours','Down','Which','Is','Can','Now','On','Against', 'Ourselves','Had', 'At','Few', 'Too', 'Some', 'So', 'All', 'Them', 'While','Only','During', 'The', 'Under', 'Were', 'By', 'Further',
                       'Him', 'Because', 'Myself', 'Than', 'We', 'Have', 'Of', 'In', 'Not', 'Those', 'Are', 'Hers', 'Was', 'Out', 'No','Off', 'Itself','Or', 'These', 'Where', 'Just', 'Then', 'You', 'There', 'After', 'Again', 'Its',
                       'When', 'And', 'Being', 'Any', 'Same', 'Theirs','Own', 'Up', 'More', 'A', 'His', 'As', 'Yourselves', 'Our', 'Such', 'She', 'Why', 'An', 'Be','Over','Into', 'Nor', 'But', 'Most', 'Did', 'each', 'Shouldn','Will', 'Herself', 'Won', 'Your', 'Above', 'He', 'Should', 'Themselves',
                       'Other', 'Himself', 'Yourself', 'Her', 'Here', 'Through', 'How', 'For', 'Both', 'It', 'Has', 'Until', 'Before', 'My', 'Do', 'Between', 'About', 'Does'))

    for n in range(0,len(tokens)):
        test=[]
        for o in range(0,len(tokens[n])):
            if tokens[n][o].lower() not in stop_words:
                test.append(tokens[n][o].lower())
        filtered.append(test)


    #df_Comment Builder
    for p in range(0, len(filtered)):
        df_Comment[p]=' '.join(filtered[p])
    #
    # for test in range(0,len(sym_removal)):
    #     df_Comment[test]=sym_removal[test]

    return df_Comment,df_Category











