//IBMUSER1 JOB (SYSP,1),'IBMUSER',MSGCLASS=X,                           00010000
//            NOTIFY=&SYSUID                                            00020000
//*                                                                     00030000
//* BATCH REXX CHANGE ALL                                               00040000
//*                                                                     00050000
//STEP1    EXEC PGM=ICEGENER                                            00060000
//SYSIN    DD DUMMY                                                     00070000
//SYSPRINT DD SYSOUT=*                                                  00080000
//SYSUT2   DD UNIT=SYSALLDA,DSN=&&SYSEXEC(MYREXX),  ===                 00090000
//           DISP=(MOD,PASS),SPACE=(CYL,(1,1,10)),                      00100000
//           DCB=(SYS1.MACLIB,BLKSIZE=0)                                00110000
//SYSUT1   DD *                                                         00120000
 /* BATCH REXX CHANGE ALL                                        */     00130000
                                                                        00140000
 'EXECIO * DISKR FILEIN1 (STEM SKELETON.' /* READ IN SKELETON JCL */    00150000
                                                                        00160000
 'EXECIO * DISKR FILEIN2 (STEM PARM.'     /* READ IN PARAMETERS   */    00170000
                                                                        00180000
 DO IX1 = 1 TO SKELETON.0                 /* SKELETON JCL ..      */    00190000
   SKELETON.IX1 = LEFT(SKELETON.IX1, 72)  /*   REMOVE LINE NUMS   */    00200000
                                                                        00210000
   SAY SKELETON.IX1                                                     00220000
 END /* DO IX1 = 1 TO SKELETON.0 */                                     00230000
                                                                        00240000
 DO IX1 = 1 TO PARM.0                     /* TRIM PARAMETERS      */    00250000
   PARM.IX1 = STRIP(LEFT(PARM.IX1, 72), 'BOTH')                         00260000
   SAY PARM.IX1                                                         00270000
 END /* DO IX1 = 1 TO PARM.0 */                                         00280000
                                                                        00290000
 COUNTER1 = 0                                                           00300000
                                                                        00310000
 DO IX1 = 2 TO PARM.0             /* <<< PARM.1 IS VALUE IN SKELETON */ 00320000
   DO IX2 = 1 TO SKELETON.0       /* SKELETON JCL CARDS LOOP         */ 00330000
     COUNTER1 = COUNTER1 + 1                                            00340000
     OUTLINE.COUNTER1 = SKELETON.IX2 /* MOVE SKELETON TO OUTPUT LINE */ 00350000
                                                                        00360000
     COUNTER2 = POS(PARM.1, OUTLINE.COUNTER1) /* CHECK WITH PARM     */ 00370000
                                                                        00380000
     DO WHILE COUNTER2 > 0                    /* REPLACE PARAMETER   */ 00390000
       TMP1 = LEFT(OUTLINE.COUNTER1, COUNTER2-1)                        00400000
       TMP2 = SUBSTR(OUTLINE.COUNTER1, COUNTER2+LENGTH(PARM.1))         00410000
       OUTLINE.COUNTER1 = TMP1 || PARM.IX1 || TMP2                      00420000
       COUNTER2 = POS(PARM.1, OUTLINE.COUNTER1)   /* CHECK WITH PARM */ 00430000
     END /* DO WHILE COUNTER2 > 0 */                                    00440000
                                                                        00450000
   END /* DO IX2 = 1 TO SKELETON.0 */                                   00460000
 END /* DO IX1 = 1 TO PARM.0 */                                         00470000
                                                                        00480000
 'EXECIO * DISKW FILEOUT1 (STEM OUTLINE.'       /* WRITE OUTPUT JCL  */ 00490000
                                                                        00500000
 RETURN                                                                 00510000
                                                                        00520000
//*                                                                     00530000
//* EXECUTE REXX PROGRAM                                                00540000
//*                                                                     00550000
//STEP3    EXEC PGM=IRXJCL,PARM='MYREXX'            ===                 00560000
//SYSEXEC  DD DISP=(OLD,PASS),DSN=&&SYSEXEC                             00570000
//SYSTSPRT DD SYSOUT=*                                                  00580000
//FILEIN1  DD DATA,DLM=')(' SKELETON*SKELETON*SKELETON*SKELETON*        00590000
//IBMUSER3 JOB (SYSP,1),IBMUSER,MSGCLASS=X,                             00600000
//           NOTIFY=&SYSUID,                                            00610000
//*                                                                     00620000
//* RMM ADD SCRATCH VOLUME                                              00630000
//*                                                                     00640000
//RMMSTEP  EXEC PGM=IKJEFT01,DYNAMNBR=99,REGION=4M                      00650000
//SYSTSPRT DD SYSOUT=*                                                  00660000
//SYSTSIN  DD *                                                         00670000
 RMM ADDVOLUME &PARM1 COUNT(1) INITIALIZE(Y) -                          00680000
   LOCATION(LIB19) STATUS(SCRATCH) TYPE(LOGICAL)                        00690000
 RMM CHANGEVOLUME &PARM1 CONFIRMRELEASE(INIT)                           00700000
 RMM LISTVOLUME   &PARM1                                                00710000
)(                                                                      00720000
//FILEIN1X DD DATA,DLM=')(' SKELETON*SKELETON*SKELETON*SKELETON*        00730000
//IBMUSERB JOB (SYSP,1),IBMUSER,MSGCLASS=X,                             00740000
//           NOTIFY=&SYSUID                                             00750000
//*                                                                     00760000
//STEP1    EXEC PGM=IDCAMS                                              00770000
//SYSPRINT DD SYSOUT=*                                                  00780000
 ALTER V&PARM1 VOLUMEENTRY USEATTRIBUTE(SCRATCH)                        00790000
//* RMM REMOVE VOLUME                                                   00800000
//*                                                                     00810000
//STEP2    EXEC PGM=IKJEFT01,DYNAMNBR=99,REGION=4M                      00820000
//SYSTSPRT DD SYSOUT=*                                                  00830000
//SYSTSIN  DD *                                                         00840000
 RMM LISTVOLUME   &PARM1                                                00850000
 RMM DELETEVOLUME &PARM1 REMOVE /* REMOVE FROM RMM */                   00860000
 RMM ADDVOLUME    &PARM1 COUNT(1) INITIALIZE(Y) -                       00870000
   LOCATION(LIB19) STATUS(SCRATCH) TYPE(LOGICAL)                        00880000
 RMM CHANGEVOLUME &PARM1 CONFIRMRELEASE(INIT)                           00890000
 RMM LISTVOLUME   &PARM1                                                00900000
)(                                                                      00910000
//FILEIN2  DD * PARM*PARM*PARM*PARM*PARM*PARM*PARM*PARM*PARM*PARM*      00920000
 &PARM1                                                                 00930000
 XXXXXX                                                                 00940000
 XXXXXX                                                                 00950000
 XXXXXX                                                                 00960000
//FILEOUT1 DD SYSOUT=*,                                                 00970000
//           DCB=(RECFM=FB,LRECL=80,BLKSIZE=0)                          00980000
//                                                                      00990000
