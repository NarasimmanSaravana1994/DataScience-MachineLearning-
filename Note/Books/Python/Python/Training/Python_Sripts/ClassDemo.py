class human:
    "This is my doc string"
    a="My class member !!!!"

    def do_work(self,name,occupation):
        print("self is", self)
        if occupation == 'Leader':
            print(name , "is a leader")
        elif occupation == 'Olympics player':
            print(name , "is a olympics player")

    def speaks(self,name):
        print(name,"says hello !!!")

    def emptyfunction(self):
        print("hello")



##print(human.__doc__)
##print(human.a)
###human.do_work(self,"Hitler","Leader")

##hitler = human()
##hitler.do_work("Hitler","Leader")
##hitler.speaks("Hitler")
##hitler.emptyfunction()
##print(hitler.a)
##

##mar = human()
##mar.do_work("Mariappan","Olympics player")
##mar.speaks("Mariappan")
