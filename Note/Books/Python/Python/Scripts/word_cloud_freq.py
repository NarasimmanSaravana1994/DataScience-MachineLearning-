import pyodbc
import pandas as pd
import nltk
import matplotlib.pyplot as plt
import random
import warnings
import numpy as np
warnings.filterwarnings("ignore", category=DeprecationWarning)
pd.options.mode.chained_assignment = None
import TextPreProcessing
import DBConnection
import sqlite3

import re
from nltk.tokenize import TweetTokenizer

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#
#
def grey_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)



df_Comment,df_Categ=TextPreProcessing.preProcessing()


neg_text=""
pos_text=""
for i in range(0,len(df_Comment)):
    if df_Categ[i]==0:
        neg_text=neg_text+' '+df_Comment[i]
    else:
        pos_text=pos_text+' '+df_Comment[i]


tokenizer=TweetTokenizer()
neg_words=tokenizer.tokenize(neg_text)
pos_words=tokenizer.tokenize(pos_text)



#FreqDistribution of Neg
freq_dist_neg = nltk.FreqDist(neg_words)
freq_dist_pos=nltk.FreqDist(pos_words)

freq_dist_neg=freq_dist_neg.most_common(len(freq_dist_neg))
freq_dist_pos=freq_dist_pos.most_common(len(freq_dist_pos))



#
conn = sqlite3.connect("TextAnalytics.db")

c = conn.cursor()
c.execute("drop table if exists neg_pos_words")
c.execute("create table neg_pos_words(Words, Freq, Category)")


c.executemany("Insert into neg_pos_words values(?,?,'pos')",freq_dist_pos)
c.executemany("Insert into neg_pos_words values(?,?,'neg')",freq_dist_neg)
conn.commit()










#


#
#






from os import path
from wordcloud import WordCloud



######### Neg_cloud






# Generate a word cloud image
neg_wordcloud = WordCloud(background_color="Black",width=1000,height=1000,max_words=1000).generate(neg_text)



plt.imshow(neg_wordcloud.recolor(color_func=grey_color_func,random_state=3), interpolation='bilinear')
plt.axis("off")

#plt.show()
plt.savefig("wordcloud.png")

### Base64 String Generation
import base64
from base64 import decodebytes
with open("wordcloud.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
#print(encoded_string)



with open("foo.png","wb") as f:
    f.write(decodebytes(encoded_string))
#
################### Pos_Cloud


d = path.dirname(__file__)



# Generate a word cloud image
pos_wordcloud = WordCloud(background_color="Black",width=1000,height=1000,max_words=1000).generate(pos_text)


import matplotlib.pyplot as plt
plt.imshow(pos_wordcloud.recolor(color_func=grey_color_func, random_state=3), interpolation='bilinear')
plt.axis("off")


plt.show()

############ Word_cloud


text=""
for i in range(0,len(df_Comment)):
    text=text+" "+df_Comment[i]


from os import path
from wordcloud import WordCloud

d = path.dirname(__file__)



# Generate a word cloud image
wordcloud = WordCloud(background_color="Black",width=1000,height=1000,max_words=1000).generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3), interpolation='bilinear')
plt.axis("off")


plt.show()


# lower max_font_size
# wordcloud = WordCloud(max_font_size=40).generate(text)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")






