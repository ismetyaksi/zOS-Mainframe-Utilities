#!/usr/bin/python3

# zOS DFSMS Listings

# ruler
#...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8

def read_line(file_input):
    line_input = file_input.readline()
    line_input = line_input.rstrip()          # remove newline
    return(line_input)

def write_line(file_output, line_output):
    file_output.write(line_output + "\n")
    return()

pseudo_eof = ")("

delim1 = ";"
delim2 = "_"

header1 = "dfsms listings "                   # <<<
header2 = header1.replace(" ", delim2)

file_input1  = open("aa_" + header2 + "filein1.txt", "r")
file_output1 = open("zz_" + header2 + "fileout1.txt", "w")
#file_output2 = open("zz_" + header2 + "fileout2_skipped.txt", "w")

n_newpage           = 0
n_type_hdr          = 0

type_header         = ""
separator_column    = 99

object_name_to_come = 0

list_object         = []
object_name         = ""

list_label_num      = []
list_label_value    = []

# start of mainline # start of mainline # start of mainline # start of mainline 

# 1. All lines of reports are read one by one.

line_input1 = read_line(file_input1)        # read next input line

while (line_input1 != pseudo_eof):

    line_input1 = line_input1.lstrip()

# 2. New page headers are discarded.

    if (line_input1 == "1"):
        n_newpage += 1

# 3. Report types are extracted from heading lines.
        
    elif ("ISMF" in line_input1) and ("List" in line_input1):
        n_type_hdr += 1
        line_input1 = line_input1.replace("-", " ")
        type_header = line_input1.strip()
        type_header = type_header[5:-5]         # drop ISMF & List

        if (type_header == "Volume"):           # set separator column
            separator_column = 31
        elif (type_header == "Management Class"):
            separator_column = 37
        elif (type_header == "Data Class"):
            separator_column = 35
        else:   # type_header equals "Storage Class"
            separator_column = 36

# 4. Object names (volume, management class, data class and
#   storage class names) are found after null lines.

    elif (line_input1 == ""):
        object_name_to_come = 1
    elif (object_name_to_come == 1):
        if (line_input1 == ("-" * 66)) or (line_input1 == ("-" * 62)):
            pass
        else:
            object_last = line_input1.strip()
            #write_line(file_output1, "1 >>> " + object_last)
            if (object_last == object_name):
                pass
            else:
                if (list_object != []):
                    write_line(file_output1, delim1.join(list_object))
                list_object = []
                list_object.append(type_header)
                object_name = object_last
                list_object.append(object_name)
        object_name_to_come = 0

# 5. Object information (sequence number, parameter name and parameter value)
#   displayed in one line  are extracted.

    elif (line_input1[:1] == "("):          # process columns
        label_num   = line_input1[:6]
        label_hdr   = line_input1[6:separator_column]
        label_value = line_input1[separator_column + 2:]

        label_num   = label_num.strip()
        label_hdr   = label_hdr.strip()
        label_value = label_value.strip()

# 6. Parameter values are appended to a list.
#   List is written to a CSV file when object is changed.

        if (label_value == ("-" * len(label_value))):
            label_value = ""
        elif (label_num == "(31)" and label_value == "---   / ---"):
            label_value = ""

        list_object.append(label_value)     # append column value

# 7. Sequence number and parameter name is appended to heading list.
#   List is written to a CSV file when report type changes.

        type_and_label_num = delim1.join([type_header, label_num])
        if (type_and_label_num not in list_label_num):
            list_label_num.append(type_and_label_num)
            list_label_value.append(label_hdr)

    line_input1 = read_line(file_input1)    # read next input line

write_line(file_output1, delim1.join(list_object))  # print last object

# end of mainline # end of mainline # end of mainline # end of mainline #

# 8. After completion header information is printed on console.

list_header     = []
previous_type   = ""

for ix1, tmp1 in enumerate(list_label_num):
    tmp2 = tmp1.split(delim1)

    type_header = tmp2[0]
    label_num   = tmp2[1]
    label_hdr   = list_label_value[ix1]

    print(type_header, label_num, label_hdr)

    if (type_header == previous_type):
        list_header.append( label_hdr + " " + label_num)
    else:
        if (list_header != []):
            write_line(file_output1, delim1.join(list_header))  # print header
        list_header = []
        list_header.append(type_header)
        previous_type = type_header
        list_header.append("_Object")
        list_header.append(label_hdr + " " + label_num)

write_line(file_output1, delim1.join(list_header))              # print last header

file_input1.close()
file_output1.close()

print()
print("  >>> Number of new pages", n_newpage)
print("  >>> Number of headers  ", n_type_hdr)
print()
print("  >>> EOP")
      
