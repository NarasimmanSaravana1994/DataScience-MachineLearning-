class teams:
    x=10
    def __init__(self,x,y):
        self.x = 10
        self.y ="arul"
    
    def general_categ(self):
        y="srilatha"
        print(y)
        print("WE BELONG TO TEAM DUCEN")

class COE_team(teams):
    
    def __init__(self):
        print("COE TEAM")
        self.members = 5
        self.head = "Kumar Madhavan"

    def greets(self):
        print(teams.x)
        self.general_categ()
        print("THE COE TEAM SAYS HELLO")

class ANALYTICS_team(teams):
    
    def __init__(self):
        print("ANALYTICS TEAM")
        self.members= 3
        self.head = "Mowle Asirvatham"

    def wishes(self):
        
        self.general_categ()
        print("THE ANALYTICS TEAM SAYS HELLO")


t = COE_team()
t.greets()
#t.general_categ()







        
