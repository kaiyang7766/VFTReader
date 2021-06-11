import random
from models.VFTReport import VFTReport
from reader.ReportReader import ReportReader
import csv
class CSVReader(ReportReader):
    #TODO: None
    def read(self, filepath):
        reportList = [] 
        with open(filepath, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                
                reportList.append(VFTReport(
                    row["Name"],
                    row["Eye"],
                    row["Visit"], 
                    random.randint(20, 80),
                    row["ID"],
                     #TODO: Replace age
                    row["FixLos"], 
                    row["FNRate"], 
                    row["FPRate"], 
                    row["Duration"], 
                    row["GHT"], 
                    row["VFI"], 
                    row["MD"],
                    row["MDp"],
                    row["PSD"], 
                    row["PSDp"], 
                    row["Pattern"], 
                    row["Strategy"], 
                    row["Stimulus"], 
                    row["Background"],
                    row["FoveaRefdB"],
                    self.readNumDb([row["T" + str(i)] for i in range(1, 77)], row["Eye"]),
                    self.readNumDb([row["MD" + str(i)] for i in range(1, 77)], row["Eye"]),
                    self.readNumDb([row["PSD" + str(i)] for i in range(1, 77)], row["Eye"]),
                    row["checked"]
                    ))
                line_count += 1

        return reportList

    def readNumDb(self, row, eye):
        index = 0
        graph = [[0 for i in range(10)] for j in range(10)]

        if eye.lower() == "right":
            for j in range(10):
                for i in range(10):
                    if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                        graph[i][j] = None
                    else:
                        if row[index] == "NA":
                            graph[i][j] = None
                        else:
                            graph[i][j] = row[index]
                        
                        index +=1

        else:
            for j in range(10):
                for i in range(9, -1, -1):
                    if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                        graph[i][j] = None
                    else:
                        if row[index] == "NA":
                            graph[i][j] = None
                        else:
                            graph[i][j] = row[index]
                        
                        index +=1
        return graph
