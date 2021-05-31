
class PatientData:
    def __init__(self):
        self.ID = None
        self.eyeSide = None
        self.datetime = None
        self.age = None

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