#!/usr/bin/python3

# prepare parameter definitions for IDCAMS LISTCAT

with open("aa_idcams_listcat_2parameters.txt", "r") as file_input1:
    for n_rec, line_input1 in enumerate(file_input1, start=0):
        line_input2 = line_input1.rstrip()      # remove newline

        upper_spc = line_input2.replace("-", " ")
        lower1 = line_input2.lower()
        lower1 = lower1.replace("%", "")
  
        lower_spc = lower1.replace("-", " ")
        lower_underlined = lower1.replace("-", "_")
        lower_underlined = lower_underlined.replace(" ", "_")
        len_parm = 18
        lower_underlined2 = lower_underlined + (" " * len_parm)
        lower_underlined2 = lower_underlined2[:len_parm]

        hdr1 = "hdr_" + lower_underlined2 + ' = "' + upper_spc + '"'
        print(hdr1)

##        len1 = "len_" + lower_underlined2 + ' = len(hdr_' + lower_underlined + ')'
##        print(len1)

        list1 = line_input2.split()
        for str1 in list1:
            lower2 = str1.lower()
            lower2 = lower2.replace("%", "")

            lower2_underlined = lower2.replace("-", "_")
            lower2_underlined = lower2_underlined.replace(" ", "_")
        

            lower2_underlined2 = lower2_underlined + (" " * len_parm)
            lower2_underlined2 = lower2_underlined2[:len_parm]

            lbl1 = "lbl_" + lower2_underlined2 + ' = "' + str1 + '"'
            print(lbl1)

            len1 = "*len_" + lower2_underlined2 + ' = len(lbl_' + lower2_underlined + ')'
            print(len1)

        print()
            
