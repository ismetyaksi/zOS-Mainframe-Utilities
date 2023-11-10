 /* REXX RXSLOGFL - FILTER ZOS OPERLOG/ SYSLOG MESSAGES */

 ARG MY_SYSNAME PARM2

 SAY 'SYSNAME................:' MY_SYSNAME

 IF LEFT(MY_SYSNAME, 3) = 'MAS' THEN
   WRITE_CONTROL_CHARACTER = 0  /* BATCH SDSF SYSLOG PRINT */
 ELSE
   WRITE_CONTROL_CHARACTER = 0  /* IEAMDBLG OPERLOG PRINT */

 SAY 'WRITE CONTROL CHARACTER:' WRITE_CONTROL_CHARACTER

 DELIM1 = '%'

 FIRST_LINES = '%M %MR%N %NC%NI%W %X %'  /* PRIMARY MESSAGE TYPES */
 CONT_LINES  = '%D %DR%E %ER%LR%NR%S %SC%SR%' /* CONT. REQUESTS */

 N_INPUT     = 0
 N_PAGE      = 0
 N_1ST_LINE  = 0
 N_CONT_LINE = 0
 N_MSG       = 0
 N_SKIPPED   = 0
 N_SELECTED  = 0

 CALL LIST_OF_SKIPPED_MESSAGES

 'EXECIO 1 DISKR SYSUT1 (STEM LINE_INPUT.'

 IF LEFT(LINE_INPUT.1, 7) = 'ILG0001' THEN
   DO
     SAY
     SAY '>>> INFORMATION MESSAGE OF IEAMDBLG PROGRAM SKIPPED'
     SAY
     SAY LINE_INPUT.1
     SAY

     'EXECIO 1 DISKR SYSUT1 (STEM LINE_INPUT.'
   END

 /*Y '....+....1....+....2....+....3....+....4....+....5....+....6'*/

 DO WHILE RC=0
   N_INPUT = N_INPUT + 1

   TYPE_N_REQUEST = DELIM1 || SUBSTR(LINE_INPUT.1, 1, 2) || DELIM1

   SELECT
     WHEN POS(TYPE_N_REQUEST, FIRST_LINES) <> 0 THEN
       DO
         CALL PROCESS_PREV_MSG

         CALL ADD_PRIMARY_MESSAGE_LINE

         DROP MSG_LINES.

         N_1ST_LINE = N_1ST_LINE + 1
         IX1 = 1
         MSG_LINES.IX1 = LINE_INPUT.1
         MSG_LINES.0   = IX1
       END
     WHEN POS(TYPE_N_REQUEST, CONT_LINES) <> 0 THEN
       DO
         CALL ADD_CONTINUATION
         N_CONT_LINE = N_CONT_LINE + 1
       END
     OTHERWISE
       DO
         SAY '***' LINE_INPUT.1
         SAY '***'
         SAY '*** LINE WITH UNDEFINED MESSAGE TYPE'
         SAY '*** LINE WITH UNDEFINED MESSAGE TYPE'
         SAY '*** LINE WITH UNDEFINED MESSAGE TYPE'

         EXIT 4
       END
   END /* SELECT */

   'EXECIO 1 DISKR SYSUT1 (STEM LINE_INPUT.'
 END /* DO WHILE RC=0 */

 CALL PROCESS_PREV_MSG     /* WRITE LAST MESSAGE */

 SAY
 SAY 'NUMBER OF INPUT RECORDS:' N_INPUT
 SAY 'NUMBER OF PAGES........:' N_PAGE
 SAY 'NUMBER OF PRIMARY TYPE.:' N_1ST_LINE
 SAY 'NUMBER OF CONTINUATIONS:' N_CONT_LINE
 SAY 'NUMBER OF MESSAGES.....:' N_MSG
 SAY 'NUMBER OF SKIPPED MSGS.:' N_SKIPPED
 SAY 'NUMBER OF SELECTED MSGS:' N_SELECTED

 RETURN
 RETURN

 LIST_OF_SKIPPED_MESSAGES:
   'EXECIO * DISKR SLOGLIST (STEM LIST_TO_SKIP. FINIS'

   N_SKIPLIST = 0

   TABLE_SKIPPED = DELIM1

   DO IX1 = 1 TO LIST_TO_SKIP.0
     IF LEFT(LIST_TO_SKIP.IX1, 1) <> '*' THEN /* COMMENTS CONSIDERED */
       DO
         N_SKIPLIST = N_SKIPLIST + 1
         PARSE VAR LIST_TO_SKIP.IX1 TMP1A TMP1B
         TABLE_SKIPPED = TABLE_SKIPPED || TMP1A || DELIM1
       END
   END /* DO IX1 = 1 TO N_LIST_SKIP */

   SAY 'NUMBER OF SKIPLIST.....:' N_SKIPLIST
   SAY 'TABLE OF SKIPPED MSGS..:' TABLE_SKIPPED

 RETURN

 PROCESS_PREV_MSG:
   N_MSG = N_MSG + 1

   TMP1 = SUBSTR(MSG_LINES.1, 57)
   PARSE VAR TMP1 TMP1A TMP1B TMP1C
   IF LEFT(TMP1A, 1) = '-' THEN
     DO
       IF (LEFT(TMP1A, 4) = '-STA') | (LEFT(TMP1A, 4) = '-STO') THEN
         NOP               /* DO NOT SKIP SUBSYSTEM COMMANDS */
       ELSE
         TMP1A = '-'       /* SKIP SMF EXIT STATEMENTS */
     END /* IF LEFT(TMP1A, 1) = '-' THEN */

   MSG_ID = DELIM1 || TMP1A || DELIM1

   IF POS(MSG_ID, TABLE_SKIPPED) = 0 THEN
     DO
       N_SELECTED = N_SELECTED + 1
       'EXECIO * DISKW SELECTED (STEM MSG_LINES.'
     END
   ELSE  /* POS(MSG_ID, TABLE_SKIPPED) <> 0 */
     DO
       N_SKIPPED = N_SKIPPED + 1
       'EXECIO * DISKW SKIPPED (STEM MSG_LINES.'
     END

 RETURN

 ADD_PRIMARY_MESSAGE_LINE:
   DROP MSG_LINES.

   N_1ST_LINE = N_1ST_LINE + 1

   IX1 = 1
   MSG_LINES.IX1 = LINE_INPUT.1
   MSG_LINES.0   = IX1
 RETURN

 ADD_CONTINUATION:
   IX1           = MSG_LINES.0 + 1
   MSG_LINES.IX1 = LINE_INPUT.1
   MSG_LINES.0   = IX1
 RETURN

 RETURN

