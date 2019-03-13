# PROCESS CA TOP SECRET LIST ACIDS LISTING === 2019 MARCH

# Python and IDLE v3.7.2, Tk v8.6.8 (32 bit)

# LIST Function—Display ACID Security Data
#   CA Top Secret® for z/OS - 16.0
#   https://docops.ca.com/ca-top-secret-for-z-os/16-0/en/using/issuing-commands-to-communicate-administrative-requirements/command-functions/list-functiondisplay-acid-security-data

# Writing JCL for command execution
#   IBM® z/OS 2.3.0 TSO/E Customization Executing the terminal monitor program
#   https://www.ibm.com/support/knowledgecenter/SSLTBW_2.3.0/com.ibm.zos.v2r3.ikjb400/xtmpjcl.htm

# Copying a joblog to a data set
#   IBM® z/OS 2.3.0 z/OS Management Facility Online Help Problem Determination Incident Log task Viewing diagnostic details View Diagnostic Details page Diagnostic Data tab New Attachment page
#   https://www.ibm.com/support/knowledgecenter/SSLTBW_2.3.0/com.ibm.zosmfincidentlog.help.doc/izuP00hpActCopyJLtoDS.html

# Printing from SDSF Panels
#   IBM® z/OS 2.3.0 SDSF User's Guide Introduction to SDSF
#   https://www.ibm.com/support/knowledgecenter/SSLTBW_2.3.0/com.ibm.zos.v2r3.isfa600/useprt.htm

# SUBROUTINE PROCESS SEGMENT NAME

def processSegment (segmentHeader):
    segmentName = segmentHeader
    if (segmentName[:8] == "SEGMENT "):
        segmentName = segmentName[8:]
    #print("segment " + segmentName)
    return (segmentName)

# SUBROUTINE TO WRITE PARAMETER LINE

def writeParameter (fileout1, outline1):
    fileout1.write(outline1 + "\n")
    return

# EXTRACT RESOURCE PARM VALUES

def resourceParm (parmName, parmValue, parmCount):
    if (parmName in parmValue):
        ix1 = parmValue.index(parmName)
        returnParm = parmValue[ix1+parmCount]
    else:
        returnParm = ""
    return(returnParm)

# MAINLINE

delimiter1 = ";"                        # DEFAULT OUTPUT FILE DELIMITER

# STEP 1 -- ARRANGE LISTING AS ONE PARM EACH LINE

fileout1 = open("aa2_list_acids_without_continuation_lines.txt", "w")

previousRecordString  = ""
previousRecordColumn1 = ""
previousSegment       = ""

processFile = 0                         # SKIP MESSAGES BEFORE AND AFTER LISTING

with open("aa1_list_acids.txt", "r") as filein1:
    for inputLine1 in filein1:
        inputLine1 = inputLine1[1:]             # DELETE WRITE CONTROL CHARACTER
        inputLine1 = inputLine1.rstrip("\n")    # STRIP NEWLINE
        recordColumn1 = inputLine1[:13]
        recordColumn2 = inputLine1[13:]

        if (recordColumn1 == "ACCESSORID = "):                          # START PROCESSING RECORDS
            segmentName = processSegment("Base")
            processFile = 1
        elif (inputLine1 == "TSS0300I  LIST     FUNCTION SUCCESSFUL"):  # STOP PROCESSING RECORDS
            processFile = 0

        if (processFile == 0):                              # MESSAGES ETC .. DO NOT PROCESS THE LINE
            pass
        elif (inputLine1.strip() == ""):                    # BLANK LINE
            pass
        elif (inputLine1[:1] == " "):                       # APPEND CONTINUATION AFTER PREV. LINE
            #print("append " + recordColumn1)
            previousRecordString = previousRecordString + inputLine1
            pass
        elif (recordColumn1 == previousRecordColumn1) and (recordColumn1[:3] != "XA "):      # APPEND PARAMETERS AFTER PREV. LINE
            #print("append parm " + recordColumn1)
            previousRecordString = previousRecordString + " " + recordColumn2
            pass
        elif (recordColumn1 == "-----------  "):            # SET SEGMENT NAME
            segmentName = processSegment(recordColumn2)
        else:                                               # PROCESS SEPERATE PARAMETER
            if (previousRecordString != ""):
                writeParameter (fileout1, previousSegment + delimiter1 + previousRecordString)
            
            previousRecordString = inputLine1
            previousSegment      = segmentName

        previousRecordColumn1 = recordColumn1

if (previousRecordString != ""):
    writeParameter (fileout1, previousSegment + delimiter1 + previousRecordString)

fileout1.close()

# STEP 2 - ANALYZE PARAMETERS

fileout1 = open("aa3_list_acids_selected_parms.txt", "w")
fileout2 = open("aa3_list_acids_skipped_parms.txt", "w")

list_parms    = []
list_parm_xa  = []
list_facility = []

with open("aa2_list_acids_without_continuation_lines.txt", "r") as filein1:
    for inputLine1 in filein1:
        inputLine1 = inputLine1.rstrip("\n")    # STRIP NEWLINE
        listTmp = inputLine1.split(delimiter1)
        segmentName = listTmp[0]
        parmLine    = listTmp[1]
        if (parmLine[11:12] == "="):
            parmName    = parmLine[:11]
            parmName    = parmName.strip()
            parmLine    = parmLine[13:]
            listTmp     = parmLine.split()
            parmLine    = " ".join(listTmp)
            parmLine    = parmLine.replace(" )", ")")

            if (parmName[:3] == "XA "):
                if (parmName not in list_parm_xa):
                    list_parm_xa.append(parmName)
            else:
                if (parmName not in list_parms):
                    list_parms.append(parmName)

            if (parmName == "FACILITY"):
                tmp1 = parmLine
                if (tmp1 not in list_facility):
                        list_facility.append(tmp1)
                
            tmp1        = segmentName + delimiter1 + parmName + delimiter1 + parmLine
            writeParameter(fileout1, tmp1)
        else:
            writeParameter (fileout2, inputLine1)

fileout1.close()
fileout2.close()

list_parms.sort()
list_parm_xa.sort()
list_facility.sort()

fileout1 = open("aa4_list_acids_headers.txt", "w")
writeParameter (fileout1, delimiter1.join(list_parms)    + "\n")
writeParameter (fileout1, delimiter1.join(list_parm_xa)  + "\n")
writeParameter (fileout1, delimiter1.join(list_facility) + ""  )
fileout1.close()

# STEP 3 - LIST USERS

listHeaders = []                        # SELECT PARMS TO PRINT
listHeaders.append("ACCESSORID")
listHeaders.append("TYPE")
listHeaders.append("CREATED")
listHeaders.append("LAST USED")
#listHeaders.append("TSOPROC")          # LATER ELIMINATED
listHeaders.append("HOME")
listHeaders.append("OMVSPGM")
listHeaders.append("UID")
listHeaders.append("TSOCOMMAND")
listHeaders.append("TSOLACCT")
listHeaders.append("TSOLPROC")
listHeaders.append("TSOLSIZE")
listHeaders.append("TSOMSIZE")
listHeaders.append("TSOUDATA")
listHeaders.append("TSOUNIT")

listDetail = []                         # INIT VALUES

for ix1 in range(len(listHeaders)):
    listDetail.append(listHeaders[ix1])

fileout1 = open("aa5_list_acids.csv", "w")

with open("aa3_list_acids_selected_parms.txt", "r") as filein1:
    for inputLine1 in filein1:
        inputLine1 = inputLine1.rstrip("\n")    # STRIP NEWLINE
        
        listTmp = inputLine1.split(delimiter1)  # SPLIT PARM AND VALUE
        segmentName = listTmp[0]
        parmName    = listTmp[1]
        parmLine    = listTmp[2]
        parmValue   = parmLine.split()

        if (len(parmValue) == 0):               # SKIP IF PARM HAS NULL VALUE
            continue

        if (parmName == listHeaders[0]):        # PRINT ACID DETAILS
            writeParameter (fileout1, delimiter1.join(listDetail))
            for ix1 in range(len(listDetail)):
                listDetail[ix1] = ""
            listDetail[0] = parmValue[0]

        for ix2 in range(len(listHeaders)):     # SELECT VALUE IF PARM ELIGIBLE
            if (listHeaders[ix2] == parmName):
                listDetail[ix2] = parmValue[0]
                break

writeParameter (fileout1, delimiter1.join(listDetail))  # PRINT LAST ACID ENTRY
fileout1.close()

# STEP 4 - LIST PERMISSIONS

fileout1 = open("aa6_list_resources.csv", "w")

listTmp = []
listTmp.append("ACID")
listTmp.append("TYPE")
listTmp.append("NAME")
listTmp.append("OWNER")
listTmp.append("ACCESS")
listTmp.append("ACTION")
listTmp.append("APPLDATA")
listTmp.append("FAC")
listTmp.append("SYSID")
lineTmp = delimiter1.join(listTmp)
writeParameter (fileout1, lineTmp)

with open("aa3_list_acids_selected_parms.txt", "r") as filein1:
    for inputLine1 in filein1:
        inputLine1 = inputLine1.rstrip("\n")    # STRIP NEWLINE

        listTmp = inputLine1.split(delimiter1)  # SPLIT PARM AND VALUE
        segmentName = listTmp[0]
        parmName    = listTmp[1]
        parmLine    = listTmp[2]


        if (parmName[:3] == "XA "):
            listTmp = parmName.split()
            resourceType = listTmp[1]
            parmLine = parmLine.replace("(", " ")
            parmLine = parmLine.replace(")", " ")
            parmValue   = parmLine.split()

            resourceOwner    = resourceParm("OWNER",    parmValue, 1)
            resourceAccess   = resourceParm("ACCESS",   parmValue, 2)
            resourceAction   = resourceParm("ACTION",   parmValue, 2)
            resourceAppldata = resourceParm("APPLDATA=",parmValue, 1)
            resourceFac      = resourceParm("FAC",      parmValue, 2)
            resourceSysid    = resourceParm("SYSID",    parmValue, 2)
            
            if (len(parmValue) > 6):
                print(">>> 1 #PARM>6 " + parmLine)
                #print(">>> 2 " + resourceOwner + " " + resourceAccess + " " + resourceAction + " " + resourceAppldata + " " + resourceSysid)

            listTmp = []
            listTmp.append(acidName)
            listTmp.append(resourceType)
            listTmp.append(parmValue[0])
            listTmp.append(resourceOwner)
            listTmp.append(resourceAccess)
            listTmp.append(resourceAction)
            listTmp.append(resourceAppldata)
            listTmp.append(resourceFac)
            listTmp.append(resourceSysid)
            lineTmp = delimiter1.join(listTmp)
            writeParameter (fileout1, lineTmp)
        elif (parmName == "ACCESSORID"):
            parmValue   = parmLine.split()
            acidName = parmValue[0]

fileout1.close()

exit()
