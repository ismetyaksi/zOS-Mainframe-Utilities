#!/usr/bin/python3

# Analyze zOS IDCAMS LISTCAT Output v2

# function to extract 1st parameter and starting column for each listcat printout line

def extract_1st_word(line_input2, str1, list_dl1):
        str1 = str1.strip()
        list_dl1.append(str1)                   # 1. first parm
        ix2 = line_input2.find(str1)
        list_dl1.append(ix2)                    # 2. column number
        list_dl1.append(1)                      # 3. number of ocuurences
        list_dl1.append(line_input2.lstrip())   # 4. line

        return(list_dl1)

# function to count 1st parameter for each starting column. Also handles exceptional parameters

def decompose_line(line_input2):
    list_dl1 = []

    ix1 = line_input2.find("REC-RETRIEVED-")
    if (ix1 != -1):
        #print(" >>>",line_input2)
        str1 = line_input2[:ix1 + len("REC-RETRIEVED")]
        #print(" >>>",ix1, str1)
        list_dl1 = extract_1st_word(line_input2, str1, list_dl1)
    else:                                           # no label - value pair
        ix1a = line_input2.find("SHROPTNS(")
        if (ix1a != -1):
            #print(" >>>",line_input2)
            str1 = line_input2[:ix1a + len("SHROPTNS")]
            #print(" >>>",ix1a, str1)
            list_dl1 = extract_1st_word(line_input2, str1, list_dl1)
        else:
            ix1b = line_input2.find("--")
            if ( ix1b != -1):                                # label - value pair
                str1 = line_input2[:ix1b]
                list_dl1 = extract_1st_word(line_input2, str1, list_dl1)
            else:
                list_dl2 = line_input2.split()
                str1 = list_dl2[0]
                list_dl1 = extract_1st_word(line_input2, str1, list_dl1)

    return(list_dl1)
  
delim1 = ";"

list_1st_words = []

list_col_details = []

ix_prev_col      = 0

col0 = ""
col3 = ""
col5 = ""
col7 = ""

n_null = 0
n_hdr  = 0

# mainline

with open("aa_idcams_listcat.txt", "r") as file_input1:
    for n_rec, line_input1 in enumerate(file_input1, start=0):
        line_input2 = line_input1.rstrip()      # remove newline

        if (line_input2[0] == "1"):
            n_hdr += 1                          # count pages
        else:
            line_input2 = line_input2[1:]       # remove write control character
            #print(" >>>", line_input2)
            if (line_input2 == ""):
                n_null += 1                     # count null lines
            else:
                list_line1 = decompose_line(line_input2)

                if (list_line1[1] in [0, 3, 5, 7]) and (list_line1[0][:3] != "IDC"):
                    #print(list_line1)

                    found1 = False
                    for n_ix, list1 in enumerate(list_1st_words):
                        #print(" >>>", list1)
                        if (list_line1[0] == list1[0]) and (list_line1[1] == list1[1]):
                            list_1st_words[n_ix][2] += 1
                            found1 = True
                            break
                    if (found1 == False):
                        list_1st_words.append(list_line1)

#                   process ordered parms

                    #print("0 >>>", ix_prev_col, list_line1[1])

                    if (ix_prev_col >= list_line1[1]):
                        list_prev_col    = [col0, col3, col5, col7]
                        str_prev_col     = delim1.join(list_prev_col)
                        #print("1 >>>", str_prev_col)

                    # add if not in the list, increment if in the list

                    found1 = False
                    for n_ix, list1 in enumerate(list_col_details):
                        #print("2 >>>", list1)
                        if (str_prev_col == list1[0]):
                            list_col_details[n_ix][1] += 1
                            found1 = True
                            break
                    if (found1 == False):
                        list_col_details.append([str_prev_col, 1])

                    # end of -- add if not in the list, increment if in the list

                    ix_prev_col = list_line1[1]

                    if (list_line1[1] == 0):
                        col0 = list_line1[0]
                        col3 = ""
                        col5 = ""
                        col7 = ""
                    elif (list_line1[1] == 3):
                        col3 = list_line1[0]
                        col5 = ""
                        col7 = ""
                    elif (list_line1[1] == 5):
                        col5 = list_line1[0]
                        col7 = ""
                    elif (list_line1[1] == 7):
                        col7 = list_line1[0]
                        
#                   end of process ordered parms                        

# end of        if (list_line1[1] in [0, 3, 5, 7]) and (list_line1[0][:3] != "IDC"):

##                if n_rec > 99:
##                    break    

# === output last prev ordered parms

# end of mainline

file_output1 = open("zz_analyze1.txt", "w")

file_output1.write("\n\n\n *** In Non-Blank Column Number Order ***\n\n\n" + "\n")

import operator

list_1st_words.sort(key=operator.itemgetter(1, 0))    

for n_ix, list1 in enumerate(list_1st_words):
    list1[1] = str(list1[1])
    list1[2] = str(list1[2])               
    str1 = delim1.join(list1)
    file_output1.write(str1 + "\n")

file_output1.write("\n\n\n *** In Parameter Name Order ***\n\n\n" + "\n")

list_1st_words.sort(key=operator.itemgetter(0, 1))    

print()
print("*** Parameters ***")
print()

for n_ix, list1 in enumerate(list_1st_words):
    list1[1] = str(list1[1])
    list1[2] = str(list1[2])               
    str1 = delim1.join(list1)
    file_output1.write(str1 + "\n")

    list1[3] = list1[3][:32]
    format1 ="{:>5} {:<25}{:>5}{:>10} {:<33}"
    print(format1.format(n_ix, *list1))

file_output1.write("\n\n\n *** Parameter series ***\n\n\n" + "\n")

list_col_details.sort(key=operator.itemgetter(0))    

print()
print("*** Parameter Series ***")
print()

for n_ix, list1 in enumerate(list_col_details):
    if (n_ix == 0):
        list1 = ["Column 1;Column 2;Column 3;Column 4", "Counter"]
    list1[1] = str(list1[1])
    str1 = delim1.join(list1)
    file_output1.write(str1 + "\n")
    format1 ="{:>5} {:<64}"
    print(format1.format(n_ix, str1))

file_output1.close()


print()
print("  >>> Number of input lines ", n_rec)
print("  >>> Number of  null lines ", n_null)
print("  >>> Number of page headers", n_hdr)
print()
print("  >>> EOP")

exit()

############################################################################

# obsolete v1

with open("aa_idcams_listcat.txt", "r") as file_input1:
    for n_rec, line_input1 in enumerate(file_input1, start=0):
        line_input2 = line_input1.rstrip()      # remove newline

        if (line_input2[0] == "1"):
            n_hdr += 1
        else:
            line_input2 = line_input2[1:]       # remove write control character
            #print(" >>>", line_input2)
            if (line_input2 == ""):
                n_null += 1
            else:
                line_input2 = line_input2.replace("--", " ")
                line_input2 = line_input2.replace("-1", " ")
                line_input2 = line_input2.replace("-2", " ")
                line_input2 = line_input2.replace("(", " ")
                list_words  = line_input2.split()

                str_word1   = list_words[0]
                ix_word1    = line_input2.find(str_word1)
                
                found1 = False
                for ix2, list1 in enumerate(list_1st_words):
                    if (list1[0] == str_word1) and (list1[1] == ix_word1):
                        list_1st_words[ix2][2] += 1
                        found1 = True
                        break
                if (found1 == False):
                    list1 = []
                    list1.append(str_word1)
                    list1.append(ix_word1)
                    list1.append(1)
                    list_1st_words.append(list1)

import operator
list_1st_words.sort(key=operator.itemgetter(1, 0))    

for ix1, list1 in enumerate(list_1st_words):
    if (list1[1] == 0) and (list1[0][:3] == "IDC"):
        pass
    
    elif (list1[1] in [0, 3, 5, 7]):
        format1 ="{:<15}{:>5}{:>7}"
        print(format1.format(*list1))

#exit()

print()
print("  >>> Number of input lines ", n_rec)
print("  >>> Number of  null lines ", n_null)
print("  >>> Number of page headers", n_hdr)
print()
print("  >>> EOP")
      
