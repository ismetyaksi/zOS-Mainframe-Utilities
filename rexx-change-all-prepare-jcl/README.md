## REXX Change All Prepare JCL

Batch REXX program reads in two input files:

1.	Skeleton jobstream
2.	Parameters

Skeleton JCL statement numbers are removed. Parameter non-significant blanks are also stripped off.

Skeleton jobstream has embedded strings inserted like “&PARM1”. Skeleton jobstream is inserted after FILEIN1 DD statement.

For each parameter string, skeleton jobstream lines are copied to an output file and each occurrence of parameter string is replaced with actual parameter. Parameters are populated after FILEIN2 DD statement. Parameter indicator should be kept in the first line.

Finally output dataset is written to JES2 spool dataset through FILEOUT1 DD statement.

After completion of execution of REXX program, spool output dataset is entered in SDSF edit mode (SE command, Select Edit) and submitted to background to execute. One set of JCL cards are prepared and executed for all parameter values.

Spool output of a sample prepared jobstream is also attached.
