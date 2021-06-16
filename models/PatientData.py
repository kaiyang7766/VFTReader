
class PatientData:
    def __init__(self, eyeSide, datetime, age, ID):
        self.eyeSide = eyeSide
        self.datetime = datetime
        self.age = age
        self.ID = ID
        

    def setID(self, ID):
        self.ID = ID

    def setEyeSide(self,eyeSide):
        self.eyeSide = eyeSide

    def setDatetime(self,datetime):
        self.datetime = datetime
    def setAge(self,age):
        self.age = age

    def getID(self):
        return self.ID

    def getEyeSide(self):
        return self.eyeSide
    def getDatetime(self):
        return self.datetime
    def getAge(self):
        return self.age