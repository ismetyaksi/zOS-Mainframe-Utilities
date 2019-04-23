#!/usr/bin/env python3

# PYTHON3 - TABULATES SMPE PTF LISTINGS

# INITIALIZE LISTS

listPtf     = []
listFmid    = []
listDateApp = []
listDateAcc = []

def processSmpeList(fileType):

    # STEP1 - ANALYZE SMPE LISTING AND LIST UNIQUE PARAMETER VALUES

    fileNameInput1  = "aa_tmp_" + fileType + ".txt"         # SET FILE NAMES

    listSmpeParm = []

    with open(fileNameInput1,"r") as fileInput1:
        for stringInput1 in fileInput1:
            stringInput1 = stringInput1.rstrip('\n')        # REMOVE NEWLINE
            stringInput1 = stringInput1.rstrip()            # RIGHT STRIP BLANKS

            if (stringInput1[27:28] == "="):                # SELECT PARAMETER LINE WITH EQUAL SIGN
                str1 = stringInput1[11:27].rstrip()
                str2 = stringInput1[29:]
                tmp1 = stringInput1.split()
                if (str1 in "%TYPE%LASTUPD%STATUS%"):       # SELECT FULL LINE FOR SPECIFIC PARMS
                    smpeParm = str1 + " " + str2
                else:
                    smpeParm = str1
                if (smpeParm not in listSmpeParm):
                    listSmpeParm.append(smpeParm)

    print("\nSMPE Parameters " + fileType + "\n")
    
    for element1 in listSmpeParm:                           # LIST PARAMETERS
        print(element1)

    # STEP2 - LIST PTFS

    fileNameOutput1 = "aa_zz_skipped_"   + fileType + ".txt"

    fileOutput1 = open(fileNameOutput1, "w")                # a APPEND, w OUTPUT

    with open(fileNameInput1,"r") as fileInput1:
        for stringInput1 in fileInput1:
            stringInput1 = stringInput1.rstrip('\n')        # REMOVE NEWLINE
            stringInput1 = stringInput1.rstrip()            # RIGHT STRIP BLANKS

            if (stringInput1[11:32] == "TYPE            = PTF"):    # SELECT TYPE PARAMETER
                ptfName = stringInput1[1:8]
            elif (stringInput1[11:29] == "FMID            = "):     # SELECT FMID PARAMETER
                ptfFmid = stringInput1[29:]
            elif (stringInput1[11:29] == "          INS   = "):     # SELECT INSTALL DATE AND TIME
                ptfDate = stringInput1[29:]

                if (ptfName in listPtf):                    # IF PTF IS IN THE LIST ..
                    ix1 = listPtf.index(ptfName)
                    if (fileType == "tgt"):                 # .. AND IF TARGET LISTING ..
                        listDateApp[ix1] = ptfDate          # UPDATE APPLY DATE
                    else:   # fileType == "dlb"             # .. AND IF DLIB LISTING ..
                        listDateAcc[ix1] = ptfDate          # UPDATE ACCEPT DATE

                else:                                       # APPEND PTF IN THE LIST
                    listPtf.append(ptfName)
                    listFmid.append(ptfFmid)

                    if (fileType == "tgt"):
                        listDateApp.append(ptfDate)
                        listDateAcc.append("")
                    else:   # fileType == "dlb"
                        listDateApp.append("")
                        listDateAcc.append(ptfDate)

                ptfName = ""                                # NULLIFY PTF NAME

            else:                                           # OUTPUT SKIPPED LINES
                stringOutput1 = stringInput1
                fileOutput1.write(stringOutput1 + '\n')
                
    fileOutput1.close()

    return              # def processSmpeList(fileType):

processSmpeList("tgt")
processSmpeList("dlb")

# MERGE PTF, FMID, APPLY DATE AND ACCEPT DATE LISTS

for ix1 in range(len(listPtf)):
    listPtf[ix1] = [listPtf[ix1], listFmid[ix1], listDateApp[ix1], listDateAcc[ix1]]

# CLEAR UNNECESSARY LISTS

listFmid.clear()
listDateApp.clear()
listDateAcc.clear()

# SORT PTF LIST

listPtf.sort()

# PRINT PTF LISTING AS A CSV

##for element1 in listPtf:
##    print(element1)

# WRITE PTF LIST AS A CSV

import csv

with open("aa_zz_ptf_list.csv.txt", "w") as fileout1:
    csv_writer = csv.writer(fileout1, delimiter=";")
    csv_writer.writerows(listPtf)

exit()
