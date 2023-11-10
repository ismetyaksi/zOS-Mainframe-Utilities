ZOS OPERLOG/ SYSLOG Filtering

Mainframe system programmers and consultants would like to investigate operlog or syslog records periodically.

In a medium size mainframe shop, there are at least hundreds of thousands, if not millions, of messages written to operlog/ syslog every day.

Following set of utilities filters out regular informational messages by 95% for those who want to review them periodically and enable easy visual inspection.

For zOS mainframe concepts, please see notes at bottom.

     1  SLOGPARM - Determines the julian date of the previous day.

         1.1  it is started every day after midnight either by a job scheduler or JES2 automatic command.
         1.2  The RXDATPRM rexx program determines the previous julian date date. Writes the DAYPARM member into a PDS library as SET JCL variables. 
         1.3  Next step compresses the PDS library. If you put the parameter in the PDSE library, you will not need to compress it. We used PDS due to unavailability of cross-sysplex support for PDSE.
         1.4  // EXEC J,M=SLOGPROD step starts the next operlog/ syslog printing jobstream as the final step.
         
     2  SLOGPROD - Lists operlog/ syslog messages and command output.
     
         2.1  Gets the previous day's date as a JCL variable parameter using the JCLLIB and INCLUDE JCL statements.
         2.2  Runs the IEAMDBLG sample program found in the SYS1.PARMLIB library.
         2.3  Writes the previous day's operlog/ syslog message records to a GDG dataset.
         2.4  // EXEC J,M=SLOGFILT step starts the next filtering jobstream as the final step.
         
     3  SLOGFILT - Filters Operlog/syslog messages and command outputs.
     
         3.1  The RXSLOGFL rexx program creates a table from input specified in SLOGLIST DD dataset. Input dataset specifies regular or informational messages and console commands.
         3.2  You can use our SYSLOG analyzer utility to construct input for messages to skip
         3.3  The program constitutes multi-line messages and/or command outputs.
         3.4  To create multi-line messages, the type and request codes in the "Using the system log" section of the "zOS SDSF User's Guide" document were used.
             3.4.1  URL https://www.ibm.com/docs/en/zos/2.5.0?topic=sdsf-using-system-log
         3.5  The dataset of the last daily list of operlog/ syslog messages is defined as input to the SYSUT1 DD statement.
         3.6  It writes the regular and routine messages in the non-selection table to the dataset in the SKIPPED DD statement. This dataset can be examined periodically for diagnostic purposes.
         3.7  Other message and command outputs are written to the sysout dataset in the SELECTED DD statement. By checking the JES spool every day, exceptional messages and commands from the previous day can be easily examined.
         3.8  In our case, SLOGFILT job filters around 95% of operlog/syslog messages.

Notes on zOS Mainframe:

    1. Each mainframe instance creates a SYSLOG dataset to write all system messages and console command entries.
    2. Files in mainframe environment are called datasets.
    3. SYSLOG dataset is maintained by JES (Job Entry Subsystem) spool system.
    4. In a mainframe hardware, multiple mainframe instances are operated by virtualization.
    5. SYSPLEX (Systems Complex) is mainframe clustering with multiple instances behaving like a single mainframe.
    6. OPERLOG is the collection of all SYSLOG datasets in a SYSPLEX
    7. REXX (REstructured eXtended eXecutor) is one of script languages widely used in mainframe environment.
    8. PDS (Partitioned Dataset) and PDSE (PDS Extended) are zOS library formats. They contain either binary or text members. 
    9. System libraries start with SYS1 qualifier.
    10. GDG (Generation Date Group) is a collection of sequential data kept in choronological order.
    11. SYSLOG message is composed of message type, request code, message-ID and message text 

