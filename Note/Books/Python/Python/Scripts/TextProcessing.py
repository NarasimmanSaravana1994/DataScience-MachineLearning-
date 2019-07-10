from nltk.tokenize import sent_tokenize,word_tokenize,PunktSentenceTokenizer,WordPunctTokenizer
import os
from nltk.corpus import stopwords,state_union
from nltk.stem import PorterStemmer
import nltk


path="C:/Users/mirra.balaji/Music/TextAnalytics"
os.chdir(path)

#tokenisation
text = open("hitler.txt").read()
senToken = sent_tokenize(text)
wordToken = word_tokenize(text)
#print(text)
#print(senToken)
#print(wordToken.__len__())
#
# #stopwords
# stop_words = set(stopwords.words("english"))
# filtered = [w for w in wordToken if not w in stop_words]
# #print(filtered.__len__())
#
# #@stemming
# # po=PorterStemmer()
# # for w in wordToken:
# #     print(po.stem(w))
#
# #PunktSentenceTokenizer
# text2= state_union.raw("1975-Ford.txt")
# punkToken= PunktSentenceTokenizer().tokenize(text)
# tokenized = PunktSentenceTokenizer().tokenize(text2)
# #print(punkToken.__len__())
#
# wordpunckt=WordPunctTokenizer().tokenize(text)
# #print(wordpunckt)
#
# def process_content():
#     try:
#         for i in tokenized:
#             words = nltk.word_tokenize(i)
#             tagged=nltk.pos_tag(words)
#             chunked=r"""Chunk:{<RB.?>*<VB.?>*<NNP>+<NN>?}"""
#             chunkParser = nltk.RegexpParser(chunked)
#             chunk=chunkParser.parse(tagged)
#
#             chunk.draw()
#             #print(tagged)
#     except Exception as e:
#         print(str(e))
#
# #process_content()
#
# def process_contentC():
#     try:
#         for i in tokenized:
#             words = nltk.word_tokenize(i)
#             tagged=nltk.pos_tag(words)
#             chunked=r"""Chunk:{<.*>+}
#             }<VB.?|IN|DT|TO>+{"""
#             chunkParser = nltk.RegexpParser(chunked)
#             chunk=chunkParser.parse(tagged)
#
#
#             chunk.draw()
#     except Exception as e:
#         print(str(e))
#
# #process_contentC()
#
