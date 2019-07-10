



class AudioFile:
    
    def __init__(self,filename):
        try:
            if not filename.endswith(self.ext):
                raise Exception("Invalid Format")
            
        except Exception as e:
            print(e)
        
        self.filename= filename
        


class mp3file(AudioFile):
    
    ext="mp3"
    def play(self):
        print("playing as mp3",self.filename)

class wavfile(AudioFile):
    
    ext="wav"
    def play(self):
        print("playing as wav",format(self.filename))



##mp3 = mp3file("indhu.venkat.mp3")
##mp3.play()

ogg = mp3file("file.ogg")


##    try:
##    except Exception as e:
##            print(e)
