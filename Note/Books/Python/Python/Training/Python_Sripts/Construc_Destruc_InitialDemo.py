import datetime

###############    Normal Method :

class A:
    
    def met(self,a,b):
        self.a=a
        self.b=b
        print(self.a,self.b)
        

ob = A()
ob.met(10,20)


################  Static Method :

##class A:
##    @staticmethod
##    def met(a, b):
##        print(a, b)
##
##A.met(30,40)

################ __init__()
##
##class A:
##    def __init__(self, a, b):
##        print("init gets called")
##        print("self is", self)
##        self.a1, self.b1 = a,b
##        print(a,b)
##
##    def function(self):
##        print(self.a1)
##
##        
##
##object1 = A(50,60)
##object1.function()

##############  __new__()

##class A:
##    
##    #here we overwrite inherited new class from the super class
##    def __new__(cls, *args, **kwargs):
##
##        
##        print(cls)
##        print("args is", args)
##        print("kwargs is", kwargs)
##
##        
##    # We tried to create an instance of A and __new__ of A received
##    # class A itself as the first argument.
##    
####object2 = A()
####print(object2)
##
##object3=A(1,2,3,name=6)
##print(object3)



############# both together #########

##class A(object):
##     def __new__(cls, *args, **kwargs):
##         print(cls)
##         print(args)
##         print(kwargs)
##     def __init__(self, a, b):
##         print("init gets called")
##         print("self is", self)
##         self.a, self.b = a, b
##
##
##a=A(1,2)






