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
