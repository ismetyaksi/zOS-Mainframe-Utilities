#!/usr/bin/python3

# zOS SYSLOG Message Selection

# ruler
#...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8

delim1 = ";"

#print_limit = 0

#file_analysis = open("zz_analysis.txt", "w")

# 1. Each syslog line is read.

with open("aa_syslog.txt", "r", errors="replace") as file_input1:
    n_null     = 0
    n_newpage  = 0
    type_prim  = ""
    type_sec   = ""
    msg_id1    = ""
    list_type  = []
    list_msg   = []
    list_sec_type = []
    list_dash_cmd   = []

    for ix1, line_input1 in enumerate(file_input1, start=0):
        line_input2 = line_input1.rstrip()      # remove newline

        if (line_input2 == ""):                 # count null lines
            n_null += 1
        elif (line_input2[0] == "1"):           # count newpage headers
            n_newpage += 1

# 2. When a primary type line is read, it is either added to a list or number of occurrence is incremented.

        elif (line_input2[1:3] in ["M ", "MR", "N ", "NC", "W "]):
            type_prim = line_input2[1:3]

            type_found = 0                      # process primary message types
            for ix2, each_type in enumerate(list_type, start=0):
                if (type_prim == each_type[0]):
                    list_type[ix2][1] += 1
                    type_found = 1

            if (type_found == 0):
                list_type.append([type_prim, 1])

            msg_id1  = line_input2[57:]         # process message IDs 1/2
            msg_id1a = msg_id1.split()
            msg_id2 = msg_id1a[0]
            if (msg_id2[0] == "-"):
                #file_analysis.write(line_input2[57:] + "\n")

# 3. If the primary type line has a dash line, it is added to a list and incremented.

                type_found = 0                      # process dash cmds
                for ix5, each_dash_cmd in enumerate(list_dash_cmd, start=0):
                    if (msg_id2 == each_dash_cmd[0]):
                        list_dash_cmd[ix5][1] += 1
                        type_found = 1

                if (type_found == 0):
                    list_dash_cmd.append([msg_id2, 1])

                msg_id2 = "-"
            
##            print_limit += 1
##            if (print_limit > 100):
##                exit(0)

# 4. Messages other than dash messages are also recorded and counted.

            msg_found = 0                       # process message IDs 2/2
            for ix3, each_msg in enumerate(list_msg, start=0):
                if (msg_id2 == each_msg[0]):
                    list_msg[ix3][1] += 1
                    msg_found = 1

            if (msg_found == 0):
                list_msg.append([msg_id2, 1, msg_id1])

# 5. When a continuation message type is read, it is also recorded and counted.

        elif (line_input2[1:3] in ["D ", "DR", "E ", "ER", "LR", "NR", "S ", "SC", "SR"]):
            type_sec = type_prim + " -- " + line_input2[1:3]

            type_sec_found = 0                      # process secondary message types
            for ix2, each_sec_type in enumerate(list_sec_type, start=0):
                if (type_sec == each_sec_type[0]):
                    list_sec_type[ix2][1] += 1
                    type_sec_found = 1

            if (type_sec_found == 0):
                list_sec_type.append([type_sec, 1])

# 6. If the message and request type combination is not recognized, program issues a message and stop processing. The message type combination is expected to be added.

        else:
            print(">>> UNDEFINED", ix1, line_input2)
            tmp1 = line_input2[57:]
            tmp1 = tmp1.split()
            tmp1 = tmp1[0]
            print(">>> MESSAGE  ", tmp1)

            exit()

# 7. List of primary message types is sorted and printed.

list_type.sort()

print("\nPrimary Message Types\n")

for ix2, each_type in enumerate(list_type):
    #print(ix2, each_type)
    tmp1 = str(ix2) + delim1 + each_type[0] + delim1 + str(each_type[1])
    print(tmp1)

# 8. List of unique message IDs  is sorted and printed.

list_msg.sort()

print("\nMessages\n")

for ix3, each_msg in enumerate(list_msg):
    #print(ix3, each_msg)
    tmp1 = str(ix3) + delim1 + each_msg[0] + delim1 + str(each_msg[1]) + delim1 + str(each_msg[2])
    print(tmp1)

# 9. List of message types/ request types combinations is sorted and printed.

list_sec_type.sort()

print("\nSecondary Types\n")

for ix4, each_sec_type in enumerate(list_sec_type):
    #print(ix4, each_sec_type)
    tmp1 = str(ix4) + delim1 + each_sec_type[0] + delim1 + str(each_sec_type[1])
    print(tmp1)

# 10. List of unique dash message types is sorted and printed.

list_dash_cmd.sort()

print("\nDash Messages\n")

for ix5, each_dash_cmd in enumerate(list_dash_cmd):
    tmp1 = str(ix5) + delim1 + each_dash_cmd[0] + delim1 + str(each_dash_cmd[1])
    print(tmp1)

# 11. Program epilog

#file_analysis.close()

print()
print("  >>> Number of input lines ", ix1)
print("  >>> Number of  null lines ", n_null)
print("  >>> Number of  newpages   ", n_newpage)
print()
print("  >>> EOP")
