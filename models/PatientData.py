

class PatientData:
    """Patient's information in a VFT report.

    Attributes:
        eyeSide: The side of the eye being tested.
        datetime: The date and time of the test.
        age: The age of the patient.
        ID: The ID of the patient.
        dob: The date of birth of the patient.
        name: The name of the patient.
    """
    def __init__(self, name ,eyeSide, datetime, age, dob, ID):
        self.eyeSide = eyeSide
        self.datetime = datetime
        self.age = age
        self.ID = ID
        self.dob = dob
        self.name = name

        
  
    def setName(self, name):
        self.name = name
    def setID(self, ID):
        self.ID = ID
    def setEyeSide(self,eyeSide):
        self.eyeSide = eyeSide
    def setDatetime(self,datetime):
        self.datetime = datetime
    def setAge(self,age):
        self.age = age
    def setDOB(self, dob):
        self.dob = dob
    
    def getName(self):
        return self.name
    def getDOB(self):
        return self.dob
    def getID(self):
        return self.ID
    def getEyeSide(self):
        return self.eyeSide
    def getDatetime(self):
        return self.datetime
    def getAge(self):
        return self.age