 /* REXX SNA SERVER IP ADDRESS FROM LU NAME                      */
 
 /* LUNAME CAN BE ENTERED FROM COMMAND LINE         === 2019 JUN */

 DEBUG = 0

 SAY                                                /* FILLER */
 SAY                                                /* FILLER */
 SAY                                                /* FILLER */
 SAY '*** LU INFO ***'
 SAY

 ARG CMD_LUNAME

 IF CMD_LUNAME = '' THEN
   DO
     SAY 'LU NAME NOT ENTERED FROM COMMAND LINE.'
     SAY 'LU NAME ?'
     PULL LUNAME1 .  /* DUMMY PLACEHOLDER, A PERIOD (.), IS USED     */
                     /*   TO ISOLATE THE FIRST WORD THE USER ENTERS. */
   END
 ELSE
   DO
     LUNAME1 = CMD_LUNAME
     SAY '>>> LU NAME .......:' LUNAME1
   END

 RCC = ISFCALLS(ON)

 /* DISPLAY LU */

 CMD1 = 'DISPLAY NET,E,ID=' || LUNAME1
 CALL ISSUE_CMD

 PUNAME1 = ''

 DO IX1 = 1 TO ISFULOG.0
   TMP1 = SUBSTR(ISFULOG.IX1, 44)
   PARSE VAR TMP1 P1 P2 P3 P4 P5 P6

   IF POS(P1, ' IST172I IST635I ') <> 0 THEN
     SAY '>>>' TMP1
   ELSE IF P1 = 'IST135I' THEN
     DO
       IF DEBUG = 1 THEN
         SAY 'DEBUG >>>' TMP1
       ELSE
         NOP
       PUNAME1 = P5
       SAY '>>> PU NAME .......:' PUNAME1
     END /* ELSE IF P1 = 'IST135I' THEN */

 END /* DO IX1 = 1 TO ISFULOG.0 */


 IF PUNAME1 = '' THEN
   RETURN

 /* DISPLAY PU */

 CMD1 = 'DISPLAY NET,E,ID=' || PUNAME1
 CALL ISSUE_CMD

 DO IX1 = 1 TO ISFULOG.0
   TMP1 = SUBSTR(ISFULOG.IX1, 44)
   PARSE VAR TMP1 P1 P2 P3 P4 P5 P6

   IF P1 = 'IST1354I' THEN
     DO
       IF DEBUG = 1 THEN
         SAY 'DEBUG >>>' TMP1
       ELSE
         NOP
       DLURNAME1 = P5
       SAY '>>> DLUR NAME .....:' DLURNAME1
     END /* IF P1 = 'IST1354I' THEN */

 END /* DO IX1 = 1 TO ISFULOG.0 */

 /* DISPLAY CPNAME */

 CMD1 = 'DISPLAY NET,EE,CPNAME=' || DLURNAME1
 CALL ISSUE_CMD

 DO IX1 = 1 TO ISFULOG.0
   TMP1 = SUBSTR(ISFULOG.IX1, 44)
   PARSE VAR TMP1 P1 P2 P3 P4 P5 P6

   IF P1 = 'IST1680I' & P2 = 'REMOTE' THEN
     DO
       IF DEBUG = 1 THEN
         SAY 'DEBUG >>>' TMP1
       ELSE
         NOP
       IPADDR1 = P5
       SAY '>>> SNA IP ADDRESS :' IPADDR1
     END /* IF P1 = 'IST1680I  THEN */

 END /* DO IX1 = 1 TO ISFULOG.0 */

 RCC = ISFCALLS(OFF)

 RETURN

 ISSUE_CMD:
   IF DEBUG = 1 THEN
     SAY 'DEBUG >>> ' || CMD1
   ELSE
     NOP
   CMD1 = "'" || CMD1 || "' (WAIT)"
   ADDRESS SDSF ISFSLASH CMD1
 RETURN
