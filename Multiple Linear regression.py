
import math


#      Y= b0 + b1*x1 + b2*x2 + b3*x3 +…… bn*xn
x = [1,2,3,4,5]
x1 = [1,2,3,4,5]
y = [2,4,5,4,5]
ypredict = []


totalValu = []

totalValu.append(x) 
totalValu.append(x1) 

def mean(column):
    mean = 0
    count = 0
    for index,val in enumerate(column):
        mean = mean + val
        count = index
        
    length = count + 1 
    return mean / length

def xymean(x,meanx):
    xx = []
    for index,val in enumerate(x):
        xx.append(val - meanx)
    return xx

def b1value(xmean,ymean):
    b1va = []
    for index,val in enumerate(ymean):
        b1va.append(xmean[index] * val)
    xsquare = []
    for index,val in enumerate(xmean):
        xsquare.append(val * xmean[index])

    return sum(b1va) / sum(xsquare)

def predict_bo(ymean,b1,b1x):
    a = []
    b0 = []
    for va in b1x:
        a.append(va * b1)

    for val in a:
        b0.append(ymean - val)
    return b0

def predict(b0,b1,val):
    predict = []
    for index,value in enumerate(val):
            predict.append(b0[index] + (b1 * value))
    return predict
   
def median(bo):
    mead=0
    count=0
    for index,val in enumerate(bo):
        mead=mead+val
        count=index
    return mead/(count+1)

def calculateRSquare(ymean,y,x):
    a=xymean(y,ymean) 
    b=[]
    for index,val in enumerate(a):
        b.append(val*a[index])
    yY=sum(b)



def multiple_linear_regression(y,totalValu):
    ymean = mean(y)
    yymean = xymean(y,ymean)
    actual = []
    predictval=[]
   

    for index,val in enumerate(totalValu):      
      b1 = b1value((xymean(totalValu[index], mean(totalValu[index]))),yymean)
      b0 = predict_bo(ymean,b1,totalValu[index])
      predictval=predict(b0,b1,val)

      actual.append(predictval)     
      rsquare=calculateRSquare(ymean,y)

    print("intercept: ",median(b0))
    print("coefficeint",b1)
    #return multipleLinearFormula(actual,b0)
    
    
    
print(multiple_linear_regression(y,totalValu))