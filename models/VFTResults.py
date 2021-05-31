
class VFTResults:
    def __init__(self, GHT, VFI, MD, PSD):
        self.GHT = GHT
        self.VFI = VFI
        self.MD = MD
        self.PSD = PSD
        
    def getGHT(self):
        return self.GHT
    def getVFI(self):
        return self.VFI
    def getMD(self):
        return self.MD
    def getPSD(self):
        return self.PSD
    def setGHT(self,GHT):
        self.GHT = GHT
    def setVFI(self,VFI):
        self.VFI = VFI
    def setMD(self,MD):
        self.MD = MD
    def setPSD(self,PSD):
        self.PSD = PSD