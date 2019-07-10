##class father:
##    def driving(self):
##        print("I like to drive cars")
##
##class mother:
##    def cooking(self):
##        print("i like to cook")
##
##class child(father,mother):
##    def sports(self):
##        print("i njoy playing")
##
##c= child()
##c.sports()
##c.cooking()
##c.driving()


class father:
    def skill(self):
        print("driving, fishing")

class mother:
    def skill(self):
        print("cooking,art")

class child(father,mother):
    def skill(self):
        father.skill(self)
        mother.skill(self)
        print("sports,eating")

c= child()
c.skill()

