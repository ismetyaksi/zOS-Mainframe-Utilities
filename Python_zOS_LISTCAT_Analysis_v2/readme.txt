Python Programs to Analyze and Tabulate zOS LISTCAT Output

Python programs analyze the zOS mainframe operating system LISTCAT utility output and convert the parameters into a CSV file. 

With the help of the spreadsheet obtained from this file and the filters to be applied, it becomes easier to examine the CLUSTER and AIX (Alternate Index) datasets in the zOS catalogs.

Programs are verified with Python 3.11.6, Ubuntu Desktop 23.10, LibreOffice Community x86_64 7.6.4.1 and z/OS v2.4

Steps To Obtain Spreadsheet with Catalog Objects

1. Prepare and execute a LISTCAT batch job similar to below job stream.

//YOURJOB  JOB  YOUR INSTALLATION'S JOB=ACCOUNTING DATA
//STEP1    EXEC PGM=IDCAMS
//SYSPRINT DD   SYSOUT=A
//SYSIN    DD   *
 LISTCAT ALL CATALOG(CATALOG.NAME#1.Vvolser)
 LISTCAT ALL CATALOG(CATALOG.NAME#2.Vvolser)
 LISTCAT ALL CATALOG(CATALOG.NAME#3.Vvolser)
 :
/*

2.  From SDSF panels display output and print SYSPRINT spool dataset to a disk dataset using XDC command.

3. Transfer dataset to workstation. Put in the folder Python programs reside. Rename as "aa_idcams_listcat.txt"

4. Execute Python program "py_idcams_listcat_3tabulate.py". CSV output will be put in the file "zz_fileout_3tabulate_1objects.txt".

5. Import CSV file to a spreadsheet program, apply filters from "OBJECT TYPE" to "SPACE TYPE" columns, freeze first row and column as headers.

Python Program Descriptions

1. py_idcams_listcat_1analyze.py

Input file: aa_idcams_listcat.txt
Output file: zz_analyze1.txt
Printout: similar to below statements:
  --- Number of input lines  1498581
  --- Number of  null lines  9
  --- Number of page headers 31698

  --- EOP

Program analyzes LISTCAT output.

First parameter in each LISTCAT report line and starting column number are determined. Full line for first occurrence and total number of occurrences are written to output file. Two sets of output are written in the following sort order:

*  First parameter column number
* Parameter name

2. py_idcams_listcat_2parameters.py

Input file: aa_idcams_listcat_2parameters.txt
Output file: none 
Printout: similar to below statements:
:
hdr_splits_ca          = "SPLITS CA"
lbl_splits_ca          = "SPLITS-CA"
*len_splits_ca          = len(lbl_splits_ca)

hdr_freespace_ci       = "FREESPACE %CI"
lbl_freespace_ci       = "FREESPACE-%CI"
*len_freespace_ci       = len(lbl_freespace_ci)
:

Program prepares CSV header and text comparison strings and print to IDLE shell.  String constants will be added to tabulate program.

3. py_idcams_listcat_3tabulate.py

Input file: aa_idcams_listcat.txt
Output files:
* zz_fileout_3tabulate_1objects.txt
* zz_fileout_3tabulate_2messages.txt (Used for debugging purposes, temporary write statements were commented out)
Printout: similar to below statements:
  --- Number of input lines..... 1498581
  --- Number of  null lines..... 9
  --- Number of page headers.... 31689
  --- Number of catalog objects. 10795

  --- EOP

Program writes CSV header line.

All lines are read one by one, page headers and message lines are skipped, parameter lines of each catalog object appended to a single string.

Whenever a new catalog object listing is started, parameters in the previous object are processed and written to output file.

At the end of input file parameters of last catalog object are processed and written to output file.

z/OS Mainframe Related Links

Using a Job to invoke IDCAMS (IDC Access Method Services)
https://www.ibm.com/docs/en/zos/3.1.0?topic=iams-using-job-job-step-invoke-access-method-services

LISTCAT command lists catalog entries
https://www.ibm.com/docs/en/zos/3.1.0?topic=commands-listcat

Copying a joblog to a data set
https://www.ibm.com/docs/en/zos/3.1.0?topic=page-copying-joblog-data-set

ismet Yaksi, ITILF Github Page
https://github.com/ismetyaksi/zOS-Mainframe-Utilities/actions
