import math

#Corelation formula 
def Internal_correlation(x,y):
    xy=[]
    for index,value in enumerate(x):
        xy.append(value * y[index])
    X=[]
    for value in x:
        X.append(value*value)
    Y=[]
    for value in y:
        Y.append(value*value)
        
    return(((sum(xy)*len(x))-(sum(x)*sum(y)))/math.sqrt(((sum(X)*len(x))-(sum(x)*sum(x)))*((sum(Y)*len(x))-(sum(y)*sum(y)))))
    
    
    
#Multiple argument handeling for y
def Correlation(x,y):
    for value in y:
        print(Internal_correlation(x,value))
    
    

#Sample arguments
x = [43,21,25,42,57,59]
y = [[99,65,79,75,87,81],[99,65,79,75,87,81],[99,65,79,75,87,81]]



# Calling the fucntion
Correlation(x,y)
