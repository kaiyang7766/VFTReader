from abc import *
from models.VFTReport import VFTReport
from ReportWriter import ReportWriter
import csv, os


class CSVWriter(ReportWriter):

    def write(self, reportList, filepath):
        with open(filepath , "w", newline='') as outf:
            writer = csv.DictWriter(outf, ['ID','File name', 'Name','Date of Birth','Age', 'Visit', 'Eye', 'Pattern', 'Strategy', 'Stimulus', 'Background', 'Duration', 'FixLos', 'FixTst', 'FNRate', 'FPRate', 'MD', 'MDp', 'PSD', 'PSDp', 'VFI', 'GHT', 'FoveaRefdB', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12', 'T13', 'T14', 'T15', 'T16', 'T17', 'T18', 'T19', 'T20', 'T21', 'T22', 'T23', 'T24', 'T25', 'T26', 'T27', 'T28', 'T29', 'T30', 'T31', 'T32', 'T33', 'T34', 'T35', 'T36', 'T37', 'T38', 'T39', 'T40', 'T41', 'T42', 'T43', 'T44', 'T45', 'T46', 'T47', 'T48', 'T49', 'T50', 'T51', 'T52', 'T53', 'T54', 'T55', 'T56', 'T57', 'T58', 'T59', 'T60', 'T61', 'T62', 'T63', 'T64', 'T65', 'T66', 'T67', 'T68', 'T69', 'T70', 'T71', 'T72', 'T73', 'T74', 'T75', 'T76', 'MD1', 'MD2', 'MD3', 'MD4', 'MD5', 'MD6', 'MD7', 'MD8', 'MD9', 'MD10', 'MD11', 'MD12', 'MD13', 'MD14', 'MD15', 'MD16', 'MD17', 'MD18', 'MD19', 'MD20', 'MD21', 'MD22', 'MD23', 'MD24', 'MD25', 'MD26', 'MD27', 'MD28', 'MD29', 'MD30', 'MD31', 'MD32', 'MD33', 'MD34', 'MD35', 'MD36', 'MD37', 'MD38', 'MD39', 'MD40', 'MD41', 'MD42', 'MD43', 'MD44', 'MD45', 'MD46', 'MD47', 'MD48', 'MD49', 'MD50', 'MD51', 'MD52', 'MD53', 'MD54', 'MD55', 'MD56', 'MD57', 'MD58', 'MD59', 'MD60', 'MD61', 'MD62', 'MD63', 'MD64', 'MD65', 'MD66', 'MD67', 'MD68', 'MD69', 'MD70', 'MD71', 'MD72', 'MD73', 'MD74', 'MD75', 'MD76', 'PSD1', 'PSD2', 'PSD3', 'PSD4', 'PSD5', 'PSD6', 'PSD7', 'PSD8', 'PSD9', 'PSD10', 'PSD11', 'PSD12', 'PSD13', 'PSD14', 'PSD15', 'PSD16', 'PSD17', 'PSD18', 'PSD19', 'PSD20', 'PSD21', 'PSD22', 'PSD23', 'PSD24', 'PSD25', 'PSD26', 'PSD27', 'PSD28', 'PSD29', 'PSD30', 'PSD31', 'PSD32', 'PSD33', 'PSD34', 'PSD35', 'PSD36', 'PSD37', 'PSD38', 'PSD39', 'PSD40', 'PSD41', 'PSD42', 'PSD43', 'PSD44', 'PSD45', 'PSD46', 'PSD47', 'PSD48', 'PSD49', 'PSD50', 'PSD51', 'PSD52', 'PSD53', 'PSD54', 'PSD55', 'PSD56', 'PSD57', 'PSD58', 'PSD59', 'PSD60', 'PSD61', 'PSD62', 'PSD63', 'PSD64', 'PSD65', 'PSD66', 'PSD67', 'PSD68', 'PSD69', 'PSD70', 'PSD71', 'PSD72', 'PSD73', 'PSD74', 'PSD75', 'PSD76', "checked"])
            writer.writeheader()
            for report in reportList:
                writer.writerow(report.toDict())
            outf.close()
    def update(self, newReport: VFTReport, originalReportPath):
        with open(originalReportPath) as inf, open(originalReportPath[:-4] + "_temp.csv", 'w', newline='') as outf:
            reader = csv.DictReader(inf)
            writer = csv.DictWriter(outf, fieldnames= reader.fieldnames)


            writer.writeheader()
            for row in reader:
                if row["File name"] == newReport.getFileName():
                    writer.writerow(newReport.toDict())
                    writer.writerows(reader)
                    break
                else:
                    writer.writerow(row)
            outf.close()
        os.remove(originalReportPath)
        os.rename(originalReportPath[:-4] + "_temp.csv", originalReportPath)
