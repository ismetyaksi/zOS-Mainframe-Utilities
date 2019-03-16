//IBMUSER1 JOB (SYSP,1),'IBMUSER',MSGCLASS=X,                           00010000
//            NOTIFY=&SYSUID                                            00020000
//*                                                                     00030000
//* BATCH REXX PROGRAM TO REMOVE DEFECTIVE USER CATALOG RECORDS         00040000
//*                                                                     00050000
//STEP1    EXEC PGM=ICEGENER                                            00060000
//SYSIN    DD DUMMY                                                     00070000
//SYSPRINT DD SYSOUT=*                                                  00080000
//SYSUT2   DD UNIT=SYSALLDA,DSN=&&SYSEXEC(MYREXX),  ===                 00090000
//           DISP=(MOD,PASS),SPACE=(CYL,(1,1,10)),                      00100000
//           DCB=(SYS1.MACLIB,BLKSIZE=0)                                00110000
//SYSUT1   DD *                                                         00120000
 /* BATCH REXX PROGRAM TO REMOVE DEFECTIVE USER CATALOG RECORDS  */     00130000
                                                                        00140000
  N_OBJ = 0                   /* NUMBER OF CATALOG OBJECTS    */        00150000
  N_REC = 0                   /* NUMBER OF INPUT RECORDS      */        00160000
  N_CMD = 0                   /* NUMBER OF COMMANDS GENERATED */        00170000
                                                                        00180000
  CALL PRT_JOBCARD1                                                     00190000
  CALL PRT_JOBCARD2                                                     00200000
  CALL PRT_JOBCARD2C                                                    00210000
  CALL PRT_JOBCARD3                                                     00220000
                                                                        00230000
 /* MAINLINE MAINLINE MAINLINE MAINLINE MAINLINE MAINLINE MAINLINE */   00240000
                                                                        00250000
  'EXECIO 1 DISKR FILEIN1 (STEM LINEIN.'                                00260000
  DO WHILE RC = 0                                                       00270000
    N_REC = N_REC + 1                                                   00280000
                                                                        00290000
 /* IF N_REC > 9876543210 THEN X* SET TO ALLOW DEBUG EXECUTION */       00300000
 /*   SIGNAL EOP1                                              */       00310000
                                                                        00320000
    SELECT                                                              00330000
      WHEN SUBSTR(LINEIN.1, 31, 24) = 'LISTING FROM CATALOG -- ' THEN   00340000
        DO                                                              00350000
          UCAT1 = STRIP(SUBSTR(LINEIN.1, 55, 44), 'T')                  00360000
          IF PREV_USRCAT <> UCAT1 THEN                                  00370000
            DO                                                          00380000
              SAY                                                       00390000
              SAY 'USER CATALOG:' UCAT1                                 00400000
              SAY                                                       00410000
                                                                        00420000
              PREV_USRCAT = UCAT1                                       00430000
            END                                                         00440000
        END                                                             00450000
                                                                        00460000
      WHEN LEFT(LINEIN.1, 09) = ' IDC3014I' THEN                        00470000
        DO                                                              00480000
          SAY LINEIN.1                                                  00490000
        END                                                             00500000
                                                                        00510000
      WHEN LEFT(LINEIN.1, 09) = ' IDC3009I' THEN                        00520000
        DO                                                              00530000
          SAY LINEIN.1                                                  00540000
        END                                                             00550000
                                                                        00560000
      WHEN LEFT(LINEIN.1, 09) = ' IDC1566I' THEN                        00570000
     /* GO EXTRACT VOLUME INFORMATION FROM IDC1566I MESSAGE */          00580000
        CALL PRT_OBJ1                                                   00590000
                                                                        00600000
      OTHERWISE                                                         00610000
        DO                                                              00620000
          NOP                                                           00630000
        END                                                             00640000
    END /* OF SELECT */                                                 00650000
                                                                        00660000
    'EXECIO 1 DISKR FILEIN1 (STEM LINEIN.'                              00670000
  END                                                                   00680000
                                                                        00690000
 /* END OF MAINLINE * END OF MAINLINE * END OF MAINLINE */              00700000
                                                                        00710000
 EOP1:                                                                  00720000
   RETURN                                                               00730000
                                                                        00740000
 PRT_OBJ1:                                                              00750000
                                                                        00760000
 /* EXTRACT VOLUME INFORMATION FROM IDC1566I MESSAGE            */      00770000
                                                                        00780000
 /* IDC3014I CATALOG ERROR                                      */      00790000
 /* IDC3009I ** VSAM CATALOG RETURN CODE IS 50 - REASON CODE IS */      00800000
 /* IGG0CLFF-5                                                  */      00810000
 /* IDC3009I FOR %VOLU%                                         */      00820000
 /* IDC1566I ** SYS1.VVDS.V%VOLU% NOT LISTED                    */      00830000
                                                                        00840000
   SAY LINEIN.1                                                         00850000
   N_OBJ = N_OBJ + 1                                                    00860000
                                                                        00870000
   PARSE VAR LINEIN.1 P1 P2 NAME_OBJ P3                                 00880000
                                                                        00890000
   SELECT                                                               00900000
     WHEN POS('.INDEX', NAME_OBJ) <> 0 THEN                             00910000
       DO                                                               00920000
         NOP /* SKIP INDEX */                                           00930000
       END                                                              00940000
                                                                        00950000
     WHEN POS('.DATA', NAME_OBJ) <> 0 THEN                              00960000
       DO /* DATA --> CLUSTER */                                        00970000
 /*      POS1 = POS('.DATA', NAME_OBJ)                       */         00980000
 /*      NAME_OBJ = SUBSTR(NAME_OBJ, 1, POS1-1) || ,         */         00990000
 /*                 SUBSTR(NAME_OBJ, POS1+5)                 */         01000000
         DSNTYPE1 = '? DATA'                                            01010000
         CALL PRT_PARM1                                                 01020000
       END                                                              01030000
                                                                        01040000
     WHEN POS('SYS1.VVDS.V', NAME_OBJ) <> 0 THEN                        01050000
       DO /* VVDS --> RECOVERY */                                       01060000
         DSNTYPE1 = 'VVDS'                                              01070000
         CALL PRT_PARM1                                                 01080000
                                                                        01090000
         CALL PRT_PARM2                                                 01100000
                                                                        01110000
         IX2 = 1                                                        01120000
         LINEOUT.IX2 = '// COMMAND '''                                  01130000
         LINEOUT.IX2 = LINEOUT.IX2 || 'ROUTE *ALL,DISPLAY U,VOL='       01140000
         LINEOUT.IX2 = LINEOUT.IX2 || SUBSTR(NAME_OBJ, 12, 6)           01150000
         LINEOUT.IX2 = LINEOUT.IX2 || ''''                              01160000
         IX2 = IX2 + 1                                                  01170000
     /*  LINEOUT.IX2 = ' ' */                                           01180000
         LINEOUT.0 = IX2                                                01190000
         CALL PRT_PARM3                                                 01200000
                                                                        01210000
         IX2 = 1                                                        01220000
         LINEOUT.IX2 = 'ROUTE *ALL,DISPLAY U,VOL='                      01230000
         LINEOUT.IX2 = LINEOUT.IX2 || SUBSTR(NAME_OBJ, 12, 6)           01240000
                                                                        01250000
         N_CMD = N_CMD + 1                                              01260000
                                                                        01270000
         /* COMMANDS WILL BE EXECUTED 5 BY 5 */                         01280000
                                                                        01290000
         IF N_CMD // 5 = 0 THEN                                         01300000
           DO                                                           01310000
             IX2 = IX2 + 1                                              01320000
             LINEOUT.IX2 = 'DELAY=1'                                    01330000
           END                                                          01340000
         LINEOUT.0 = IX2                                                01350000
                                                                        01360000
         CALL PRT_PARM4                                                 01370000
       END                                                              01380000
                                                                        01390000
     OTHERWISE                                                          01400000
       DO                                                               01410000
         DSNTYPE1 = '? NONVSAM'                                         01420000
         CALL PRT_PARM1                                                 01430000
       END                                                              01440000
                                                                        01450000
   END /* OF SELECT */                                                  01460000
                                                                        01470000
  RETURN                                                                01480000
                                                                        01490000
 PRT_PARM1:                                                             01500000
   IX2 = 1                                                              01510000
   LINEOUT.IX2 = ' /* ' || DSNTYPE1 || ' ' || LINEIN.1 || ' */'         01520000
   IX2 = IX2 + 1                                                        01530000
   LINEOUT.IX2 = ' LISTCAT ENT(' || NAME_OBJ || ') ALL -'               01540000
   IX2 = IX2 + 1                                                        01550000
   LINEOUT.IX2 = '   CATALOG(' || UCAT1 || ')'                          01560000
                                                                        01570000
   LINEOUT.0 = IX2                                                      01580000
                                                                        01590000
   'EXECIO * DISKW FILEOUT1 (STEM LINEOUT.'                             01600000
   DROP LINEOUT.                                                        01610000
   RETURN                                                               01620000
                                                                        01630000
 PRT_PARM2:                                                             01640000
   IX2 =       1                                                        01650000
   LINEOUT.IX2 = '     DELETE' NAME_OBJ 'NOSCRATCH -'                   01660000
   IX2 = IX2 + 1                                                        01670000
   LINEOUT.IX2 = '       CATALOG(' || UCAT1 || ') '                     01680000
                                                                        01690000
   LINEOUT.0 = IX2                                                      01700000
                                                                        01710000
   'EXECIO * DISKW FILEOUT3 (STEM LINEOUT.'                             01720000
   DROP LINEOUT.                                                        01730000
   RETURN                                                               01740000
                                                                        01750000
 PRT_PARM3:                                                             01760000
   'EXECIO * DISKW FILEOUT2 (STEM LINEOUT.'                             01770000
   DROP LINEOUT.                                                        01780000
   RETURN                                                               01790000
                                                                        01800000
 PRT_PARM4:                                                             01810000
   'EXECIO * DISKW FILEOU2C (STEM LINEOUT.'                             01820000
   DROP LINEOUT.                                                        01830000
   RETURN                                                               01840000
                                                                        01850000
 PRT_JOBCARD1:                                                          01860000
   LINEOUT.1 ='//IBMUSER2 JOB (SYSP,1),'IBMUSER',MSGCLASS=X,'           01870000
   LINEOUT.2 ='//            NOTIFY=&SYSUID ,TYPRUN=SCAN    '           01880000
   LINEOUT.3 ='//STEP1    EXEC PGM=IDCAMS                   '           01890000
   LINEOUT.4 ='//SYSPRINT DD SYSOUT=*                       '           01900000
   LINEOUT.0 =4                                                         01910000
   'EXECIO * DISKW FILEOUT1 (STEM LINEOUT.'                             01920000
   DROP LINEOUT.                                                        01930000
   RETURN                                                               01940000
                                                                        01950000
 PRT_JOBCARD2:                                                          01960000
   LINEOUT.1 ='//IBMUSER3 JOB (SYSP,1),'IBMUSER',MSGCLASS=X,'           01970000
   LINEOUT.2 ='//            NOTIFY=&SYSUID,CLASS=S         '           01980000
   LINEOUT.3 ='//* EXECUTE IN ALL SYSTEMS                   '           01990000
   LINEOUT.4 ='//STEP1    EXEC PGM=IEFBR14                  '           02000000
   LINEOUT.0 =4                                                         02010000
   'EXECIO * DISKW FILEOUT2 (STEM LINEOUT.'                             02020000
   DROP LINEOUT.                                                        02030000
   RETURN                                                               02040000
                                                                        02050000
 PRT_JOBCARD2C:                                                         02060000
   LINEOUT.1 ='//IBMUSER3 JOB (SYSP,1),'IBMUSER',MSGCLASS=X,'           02070000
   LINEOUT.2 ='//            NOTIFY=&SYSUID,CLASS=S         '           02080000
   LINEOUT.3 ='//* COMMANDS ARE EXECUTED 5 BY 5             '           02090000
   LINEOUT.4 ='//COMMAND  EXEC PGM=COMMAND                  '           02100000
   LINEOUT.5 ='//STEPLIB  DD DISP=SHR,DSN=SYSPROG.APFT.LOAD  <<<'       02110000
   LINEOUT.6 ='//SYSPRINT DD SYSOUT=*                       '           02120000
   LINEOUT.7 ='//IEFRDER  DD *                              '           02130000
   LINEOUT.0 =7                                                         02140000
   'EXECIO * DISKW FILEOU2C (STEM LINEOUT.'                             02150000
   DROP LINEOUT.                                                        02160000
   RETURN                                                               02170000
                                                                        02180000
 PRT_JOBCARD3:                                                          02190000
   LINEOUT.1 ='//IBMUSER4 JOB (SYSP,1),'IBMUSER',MSGCLASS=X,'           02200000
   LINEOUT.2 ='//            NOTIFY=&SYSUID ,TYPRUN=SCAN    '           02210000
   LINEOUT.3 ='//STEP1    EXEC PGM=IDCAMS                   '           02220000
   LINEOUT.4 ='//SYSPRINT DD SYSOUT=*                       '           02230000
   LINEOUT.0 =4                                                         02240000
   'EXECIO * DISKW FILEOUT3 (STEM LINEOUT.'                             02250000
   DROP LINEOUT.                                                        02260000
   RETURN                                                               02270000
/*                                                                      02280000
//*                                                                     02290000
//* EXECUTE CATALOG LISTING                                             02300000
//*                                                                     02310000
//STEP2    EXEC PGM=IDCAMS                                              02320000
//SYSPRINT DD DISP=(,PASS),DSN=&LIST1,              ===                 02330000
//           UNIT=SYSALLDA,SPACE=(CYL,(100,100),RLSE),                  02340000
//           DCB=BLKSIZE=0                                              02350000
//SYSIN    DD *                                                         02360000
 LISTCAT ALL CATALOG(CATALOG.ZOSUCT.TESTCAT)  /* <<< SET UCAT NAME */   02370000
/*                                                                      02380000
//*                                                                     02390000
//* EXECUTE REXX PROGRAM                                                02400000
//*                                                                     02410000
//STEP3    EXEC PGM=IRXJCL,PARM='MYREXX'            ===                 02420000
//SYSEXEC  DD DISP=(OLD,PASS),DSN=&&SYSEXEC                             02430000
//SYSTSPRT DD SYSOUT=*                                                  02440000
//FILEIN1  DD DISP=SHR,DSN=&LIST1                   ===                 02450000
//FILEOUT1 DD SYSOUT=*                                                  02460000
//FILEOUT2 DD SYSOUT=*                                                  02470000
//FILEOU2C DD SYSOUT=*                                                  02480000
//FILEOUT3 DD SYSOUT=*                                                  02490000
//                                                                      02500000
