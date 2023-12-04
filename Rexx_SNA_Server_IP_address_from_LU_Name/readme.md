Rexx SNA Server IP address from LU Name

Rexx script extracts SNA server IP address of any LU terminal or printer issuing VTAM display commands.

In large enterprise SNA Extender Extender networks, help desk staff may have hard time diagnosing LU connection problems. 

Root cause of connection problems may be operator’s lack of 3270 navigation information or IP network problems.

For further information about SNA and Enterprise Extender network topologies, please see https://ismetyaksi.wordpress.com/2023/11/18/sna-appn-and-enterprise-extender-mainframe-network-topologies/

Script is used from TSO terminal. It should be added to one of SYSEXEC DD statement libraries. 

Batch exec interface can be used for further development and debugging (See note #1).

LU name may be entered as a command line parameter.

A few lines is written to prevent excessive three asterisks on the ISPF screen.

LU name is asked from operator if not entered from command line.

DISPLAY ID VTAM command is issued (See note #2) after setting SDSF command environment (See note #3).

Reply messages are evaluated one by one. IST172I and IST635I messages displaying status are echoed to terminal.

PU name is extracted from IST135I message.

Another DISPLAY ID VTAM command is issued for PU. Dependent LU requestor (DLUR) name (remote host name) is extracted from IST1354I message.

Finally a DISPLAY CPNAME enterprise extender VTAM command is issued (See note #4) and IP address of remote server  is extracted from IST1680I message.

Further action is taken using IP address of SNA server.

Notes

Note #1: Using IRXJCL to Run an Exec in MVS Batch
https://www.ibm.com/docs/en/zos/3.1.0?topic=space-using-irxjcl-run-exec-in-mvs-batch 

Note #2: DISPLAY ID command
https://www.ibm.com/docs/en/zos/3.1.0?topic=commands-display-id-command

Note #3: SDSF Issuing system commands
https://www.ibm.com/docs/en/zos/3.1.0?topic=language-issuing-system-commands-isfslash
 
Note #4: Display EE connection information by remote CPNAME
https://www.ibm.com/docs/en/zos/3.1.0?topic=commands-display-ee-command#dee__display_ee_syn_5__title__1 
