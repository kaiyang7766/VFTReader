import random
from models.VFTReport import VFTReport
import csv
class CSVReader:
    """A reader for reading extracted reports in .csv files
    """
    def read(self, filepath):
        """Reads a .csv file

        Args:
            filepath (str): The path to the .csv file

        Returns:
            List[VFTReport]: A list of reports contained in the .csv file
        """
        reportList = [] 
        with open(filepath, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                
                reportList.append(VFTReport(
                    row["File name"],
                    row["Name"],
                    row["Eye"],
                    row["Visit"], 
                    row["Age"],
                    row["Date of Birth"],
                    row["ID"],
                    row["FixLos"], 
                    row["FixTst"],
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
        """Parses the data of a numerical dB graph to the format used inside the application.

        Args:
            row (List): A list of 76 values from a numerical dB graph.
            eye (str): The eye side. 

        Returns:
            List[List[str]]: A 10x10 2D list, representing the numerical dB graph.
        """
        index = 0
        graph = [[0 for i in range(10)] for j in range(10)]

        if eye.lower() == "right":
            for i in range(10):
                for j in range(10):
                    if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                        graph[i][j] = None
                    else:
                        if row[index] == "NA":
                            graph[i][j] = None
                        else:
                            graph[i][j] = row[index]
                        
                        index +=1

        else:
            for i in range(10):
                for j in range(9, -1, -1):
                    if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                        graph[i][j] = None
                    else:
                        if row[index] == "NA":
                            graph[i][j] = None
                        else:
                            graph[i][j] = row[index]
                        
                        index +=1
        

        return graph
