# zOS Mainframe Utilities

## Python 3 program merges APPLIED and ACCEPTED PTFs from zOS SMPE PTF listings

Program performs the followings:

1. SMPE TARGET zone and DLIB zone PTF listings are obtained.
2. Obtained listings are transferred to the environment where Python installed.
3. Input files are renamed and program executed.
4. SMPE parameters in the listings are analyzed.
5. First occurrence of PTF name, FMID and INStallation date are stored in Python tables.
6. In case of the occurrence for the other zone, only INStallation date is updated.
7. Unused parameter lines are written to a SKIPPED file.
8. On completion, separate lists are combined into one list
9. PTF list is sorted by PTF name.
10. PTF list is written to a CSV file.
11. CSV file is imported to a spreadsheet program and processed.

SMPE PTF listings are obtained using following parameter line:
  LIST SYSMOD PTFS.

For further information related to SMPE LIST command, please refer to online documentation:

https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.3.0/com.ibm.zos.v2r3.gim1000/chplst.htm

Analyzed parameters can be used in creating several listing programs using this program as a skeleton.

A file of unused parameter lines is prepared for debugging purposes.

Program is tested with zOS v2.3 SMPE listing and Python and IDLE v3.7.

Note: All documentation obtained from public domain resources.

Disclaimer: All rights belong to their respective owners.

## REXX Change All Prepare JCL

Batch REXX program reads in two input files:

1.	Skeleton jobstream
2.	Parameters

Skeleton JCL statement numbers are removed. Parameter non-significant blanks are also stripped off.

Skeleton jobstream has embedded strings inserted like “&PARM1”. Skeleton jobstream is inserted after FILEIN1 DD statement.

For each parameter string, skeleton jobstream lines are copied to an output file and each occurrence of parameter string is replaced with actual parameter. Parameters are populated after FILEIN2 DD statement. Parameter indicator should be kept in the first line.

Finally output dataset is written to JES2 spool dataset through FILEOUT1 DD statement.

After completion of execution of REXX program, spool output dataset is entered in SDSF edit mode (SE command, Select Edit) and submitted to background to execute. One set of JCL cards are prepared and executed for all parameter values.

Spool output of a sample prepared jobstream is also attached.

## Tabulate CA TSS zOS User and Reources Mainframe Listing Parameters

Files:

1. tabulate-tss-zos-user&resource-listing.py  -- Python 3 program
2. tabulate-tss-zos-user&resource-listing.pdf -- Description

General Flow:

1. Run TSS list user batch jobstream on zOS environment
2. Transfer output to workstation
3. Run Python 3 program to get tabulated CSV files
4. Convert CSV files to spreadsheets

## REXX Program to Eliminate USERCAT DASD Volume Messages

During zOS USERCATALOG operations, as DASD volumes are removed from system, left out cataloged system datasets cause system warning messages. This zOS jobstream with REXX program running in zOS mainframe system prepares catalog cleanup jobstreams.

## Description

Batch JCL jobstream consists of 3 steps:

 1. Copy REXX program to a temporary source library.
 2. Create a LISTCAT USERCAT listing in a temporary sequntial data set.
 3. Execute REXX program prepares user catalog cleanup jobs.

Catalog error messages are as follows:

  IDC3014I CATALOG ERROR
  IDC3009I ** VSAM CATALOG RETURN CODE IS 50 - REASON CODE IS IGG0CLFF-5
  IDC3009I FOR ZOS011
  IDC1566I ** SYS1.VVDS.VZOS011 NOT LISTED

  IDC3014I CATALOG ERROR
  IDC3009I ** VSAM CATALOG RETURN CODE IS 50 - REASON CODE IS IGG0CLFF-5
  IDC3009I FOR ZOS017
  IDC1566I ** SYS1.VVDS.VZOS017 NOT LISTED

Three types of jobstreams are prepared from processed messages:

 1. LISTCAT jobstream is submitted to confirm unavailability of VVDS system data sets.
 2. DISPLAY VOLUME commands jobstream is submitted to confirm unavailability of DASD volumes. Two types of display commands are prepared. First type is zOS COMMAND statements. Statements in this jobstream  executes all at once. The other type of commands use CBT File number 246 ["Issue Console Commands from Batch"](http://www.cbttape.org/ftp/cbt/CBT246.zip)  program.
 3. After unavailability of data sets and volumes confirmed, DELETE jobstream is submitted to delete orphan system data sets.

 //STEP1    EXEC PGM=IDCAMS                   
 //SYSPRINT DD SYSOUT=*                       
  /* VVDS  IDC1566I ** SYS1.VVDS.VZOS011 NOT LISTED */
  LISTCAT ENT(SYS1.VVDS.VZOS011) ALL -
    CATALOG(CATALOG.ZOSUCT.TESTCAT)
  /* VVDS  IDC1566I ** SYS1.VVDS.VZOS017 NOT LISTED */
  LISTCAT ENT(SYS1.VVDS.VZOS017) ALL -
    CATALOG(CATALOG.ZOSUCT.TESTCAT)
:

 //* COMMANDS ARE EXECUTED 5 BY 5
 //STEP1    EXEC PGM=IEFBR14                  
 // COMMAND 'ROUTE *ALL,DISPLAY U,VOL=ZOS011'
 // COMMAND 'ROUTE *ALL,DISPLAY U,VOL=ZOS017'
:

 //COMMAND  EXEC PGM=COMMAND                  
 //STEPLIB  DD DISP=SHR,DSN=SYSPROG.APFT.LOAD  <<<
 //SYSPRINT DD SYSOUT=*                       
 //IEFRDER  DD *                              
 ROUTE *ALL,DISPLAY U,VOL=ZOS011
 ROUTE *ALL,DISPLAY U,VOL=ZOS017
:
 DELAY=1
:

 //STEP1    EXEC PGM=IDCAMS                   
 //SYSPRINT DD SYSOUT=*                       
      DELETE SYS1.VVDS.VZOS011 NOSCRATCH -
        CATALOG(CATALOG.ZOSUCT.TESTCAT) 
      DELETE SYS1.VVDS.VZOS017 NOSCRATCH -
        CATALOG(CATALOG.ZOSUCT.TESTCAT) 
:

## Setting Up and Executing

 1. Transfer "REXX-to-eliminate-USERCAT-DASD-VOL-msg.jcl" JCL jobstream to a zOS source library member.
 2. Modify JOB card parameters using TSO ISPF full screen editor.
 3. Specify the name of user catalog. (Line number 237)
 4. Specify name of load library of CBT COMMAND program if used. (Line number 211)
 5. SUBMIT jobstream.
 6. After completion, go to SDSF spool display panel. Enter question mark (?) to display individual spool data sets.
 7. Select FILEOUT1 spool dataset having LISTCAT catalog listing commands with SE (select with editor) option and SUBMIT prepared jobstream.
 8. Select FILEOUT2 or FILEOU2C spool dataset having DISPLAY volume commands with SE (select with editor) option and SUBMIT prepared jobstream.
 9. After confirming LISTCAT and DISPLAY jobstreams, Select FILEOUT3 spool dataset having DELETE commands with SE (select with editor) option and SUBMIT prepared jobstream.
 
## REXX Migration Tools from CA Top Secret to RACF

These two batch REXX scripts make use of the output of program in the folder *tabulate-tss-zos-user&resource-listing/* and facilitate to create RACF commands from Top Secret CSV inventory.

Before utilizing these scripts, CA Top Secret inventory is tabulated using Python program mentioned above.

ACID and Resource CSV outputs transferred back to zOS as sequential data sets.

In our example these are:

* HLSYS.RACFMIG.CSV(ACID1)
* HLSYS.RACFMIG.CSV(RESOURC1)

Output of REXX scripts are written as members of HLSYS.RACFMIG.TSOCMD PDSE data set.

## IRXRACF1.REXX.JCL

Script number one has 2 parts:

1. Analyze and list ACID types
2. Create RACF ADDGROUP, ADDUSER and CONNECT commands

In the first part, following CA Top Secret parameters are identified in analysis:

 1. ACCESSORID
 2. NAME      
 3. TYPE      
 4. CREATED   
 5. LAST USED 
 6. TSOPROC   
 7. HOME      
 8. OMVSPGM   
 9. UID       
10. TSOCOMMAND
11. TSOLACCT  
12. TSOLPROC  
13. TSOLSIZE  
14. TSOMSIZE  
15. TSOUDATA  
16. TSOUNIT   
17. ATTRIBUTES
18. DFLTGRP   
19. GROUPS    
20. PROFILES  
21. DEPT ACID 
22. DIV ACID  

In the second part, following ACID types are identified and ADDUSER/ ADDGROUP commands are created:

| ACID TYPE | RACF EQUIVALENT |
| --------- | --------------- |
| MASTER    | USER (SYSPROG)  |
| CENTRAL   | USER (SYSPROG)  |
| LIMITED   |                 |
| DIVISION  | GROUP           |
| DEPT      | GROUP           |
| USER      | USER            |
| PROFILE   | GROUP           |
| GROUP     | GROUP           |
| ZONE      | USER            |

System programmer, developer and operator users are further identified from userid (ACID) prefixes.

Top Secret DIVISION, DEPT, PROFILE and GROUP ACIDS will be defined as RACF groups.

OMVSGRP is set as owner and superior group for all groups.

Users are CONNECTED to groups to share group resources.

## IRXRACF2.REXX.JCL

Second script identifies resources and creates RDEFINE and PERMIT commands to define and give permission to resources.

Selected and incompatible resources are maintained in separate lists. TSS-only resource classes will not be generated.

Part one of script will create RDEFINE statements from CSV input.

Dataset profiles will be created using ADDSD statements.

Part two of script will create PERMIT statements from CA Top Secret raw ACID listing.

RDELETE and DELDSD command members are also prepared in case of recreation fron scratch.

For RACF ADDGROUP, ADDUSER, CONNECT, RDEFINE, ADDSD and PERMIT command syntax please see z/OS Security Server RACF Command Language Reference

(https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.3.0/com.ibm.zos.v2r3.icha400/cmdsyn.htm)
