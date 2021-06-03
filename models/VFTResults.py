
class VFTResults:
    def __init__(self, GHT, VFI, MD, MDp, PSD, PSDp):
        self.GHT = GHT
        self.VFI = VFI
        self.MD = MD
        self.PSD = PSD
        self.MDp = MDp
        self.PSDp = PSDp
        
    def getGHT(self):
        return self.GHT
    def getVFI(self):
        return self.VFI
    def getMD(self):
        return self.MD
    def getPSD(self):
        return self.PSD
    def getMDp(self):
        return self.MDp
    def getPSDp(self):
        return self.PSDp
    def setGHT(self,GHT):
        self.GHT = GHT
    def setVFI(self,VFI):
        self.VFI = VFI
    def setMD(self,MD):
        self.MD = MD
    def setPSD(self,PSD):
        self.PSD = PSD
    def setMDp(self,MDp):
        self.MDp = MDp
    def setPSDp(self,PSDp):
        self.PSDp = PSDp
    
    