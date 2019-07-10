class human:
    
    def __init__(self,n,o):
        self.name = n
        self.occupation = o
        
    def do_work(self):
        print("self is", self)
        
        if self.occupation == 'Leader':
            print(self.name , "is a leader")
        elif self.occupation == 'Olympics player':
            print(self.name , "is a olympics player")

    def speaks(self):
        print(self.name,"says hello !!!")

    def __del__(self):
        class_name = self.__class__.__name__
        print( "destroyed")

##
##hit = human("Hitler","Leader")
##hit.do_work()
##hit.speaks()
##hit.__del__()

##mar = human("Mariappan","Olympics player")
##mar.do_work()
##mar.speaks()


