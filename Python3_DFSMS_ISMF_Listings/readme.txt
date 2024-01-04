
Python Program Prepares CSV File from IBM Mainframe zOS ISMF Listings

For Mainframe Concepts see below.

ISMF Listings processed are "Volume", "Management Class", "Data Class", "Storage Class".

Obtaining listings are explained in "z/OS DFSMS Using the Interactive storage Management Facility" documentation.

Generating a DASD Volume List
https://www.ibm.com/docs/en/zos/3.1.0?topic=lists-generating-dasd-volume-list

Generating a Data Class List
https://www.ibm.com/docs/en/zos/3.1.0?topic=ismf-generating-data-class-list

There is no need to execute the final panel for each task as listing dataset is already created.  

Listing dataset names are created as follows:

ZOSUSER.Dyyddd.Thhmmssm.DASDVOLU.LIST
ZOSUSER.Dyyddd.Thhmmssm.MGMTCLAS.LIST
ZOSUSER.Dyyddd.Thhmmssm.STORCLAS.LIST
ZOSUSER.Dyyddd.Thhmmssm.STORGRPS.LIST

For ease of operation, I merged listings into one text file using following IEBGENER jobstream.

Command ===>                                                  Scroll ==
****** ***************************** Top of Data **********************
000100 //%USERID.A JOB MSGCLASS=X,REGION=4M,NOTIFY=&SYSUID
000200 //*
000300 //STEP1    EXEC PGM=ICEGENER
000400 //SYSPRINT DD SYSOUT=*
000500 //SYSIN    DD DUMMY
000600 //SYSOUT   DD SYSOUT=*
000700 //SYSUT2   DD DISP=OLD,DSN=ZOSUSER.ISMF.LISTINGS.TXT
000800 //SYSUT1   DD DISP=SHR,DSN=ZOSUSER.Dyyddd.Thhmmssm.DASDVOLU.LIST
000900 //         DD DISP=SHR,DSN=ZOSUSER.Dyyddd.Thhmmssm.MGMTCLAS.LIST
001000 //         DD DISP=SHR,DSN=ZOSUSER.Dyyddd.Thhmmssm.STORCLAS.LIST
001100 //         DD DISP=SHR,DSN=ZOSUSER.Dyyddd.Thhmmssm.STORGRPS.LIST
****** **************************** Bottom of Data ********************

I transferred text file to the workstation.

I copied text file to the folder Ptyhon program resides.

I executed Python program. A CSV file containing all reports is created.

The CSV file is suitable to insert into a spreadsheet program.

Releases of programs used:

zOS and DFSMS v2.4
Python and Idle 3.11.6 with tcl/tk 8.6.13 (64 bit)
Ubuntu 23.10 Desktop AMD 64

Program mainline flow

1. All lines of reports are read one by one.
2. New page headers are discarded.
3. Report types are extracted from heading lines.
4. Object names (volume, management class, data class and storage class names) are found after null lines.  
5. Object information (sequence number, parameter name and parameter value) displayed in one line  are extracted.
6. Parameter values are appended to a list. List is written to a CSV file when object is changed.
7. Sequence number and parameter name is appended to heading list. List is written to a CSV file when report type changes. 
8. After completion header information is printed on console.
9. Output CSV file is imported to a spreadsheet program. After sorting to column #1 (Report type) and column #2 (Object name) headers are relocated at the beginning of each report. 

Please see some introductory IBM Mainframe concepts:

1. Files are called Datasets in IBM mainframe zOS operating system environment.
2. Datasets are located on disks. Disks are called Volumes or DASD (Direct Access Storage Devices).
3. Name of disk is called "volume serial"
4. Management of datasets and disks are performed through ISMF (Interactive Storage Management Facility).
5. ISMF is a component of DFSMS (Data Facility Storage Management System) or SMS for short.

