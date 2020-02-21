class Dog:
    def __init__(self, name, month, day, year, speakText):
        self.name = name
        self.day = day
        self.year = year
        self.speakText = speakText
        self.month = month
    def speak(self):
        return self.speakText
    def getName(self):
        return self.name
    def BirthDate(self):
        return str(self.month) + "/" + str(self.day)+ "/" + str(self.year)
    def changeBark(self,bark):
        self.speakText = bark
    def __add__ (self,otherdog):
        return Dog("Puppy of" + self.name + "and" + otherdog.name , self.month, self.day , self.year + 1 , self.speakText + otherdog.speakText)

def main():
    boyDog = Dog("Mesa", 5 , 15, 2004, "WOOF")
    grilDog= Dog("sequoia", 5 , 6, 2004, "barkbark")
    print(boyDog.speak())
    print(grilDog.speak())
    print(boyDog.getName())
    print(grilDog.getName())
    print(boyDog.BirthDate())
    print(grilDog.BirthDate())
    boyDog.changeBark("WOOFywoofy")
    Puppy = boyDog + grilDog
    print(Puppy.speak())
    print(Puppy.getName())
    print(Puppy.BirthDate())
if __name__ == "__main__":
    main()
