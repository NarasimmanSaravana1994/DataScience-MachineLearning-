import math


#      Y= b0 + b1*x1 + b2*x2 + b3*x3 +…… bn*xn



x=[1,2,3,4,5]
x1=[1,2,3,4,5]
y=[2,4,5,4,5]


totalValu=[]

totalValu.append(x1)

totalValu[0]


def multiple_linear_regression(y,totalValu):
    
    
ymean=mean(y)

for index,val in enumerate(totalValu):
    print(mean(totalValu[index]))
    xymean(totalValu[index],mean(totalValu[index]))
          
    
    
    
def mean(column):
    mean=0
    count=0
    for index,val in enumerate(column):
        mean=mean+val
        count=index
        
    length=count+1 
    return mean/length


def b1(x,meanx):
    for 
    
    
    
def xymean(x,meanx):
    xmxmean=[]
    for index,val in enumerate(x):
        xmxmean.append(val-meanx)
        
   return xmxmean
        
    
def test():
    xx=[]
    xx.append(1)
    return xx