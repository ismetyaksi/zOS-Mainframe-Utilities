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
