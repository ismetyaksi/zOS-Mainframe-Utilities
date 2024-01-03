#!/usr/bin/python3

# Tabulate zOS IDCAMS LISTCAT Parameters for CLUSTERs and AIXs v2.0

#...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8

def write_line(file1, str1):
    file1.write(str1 + "\n")
    return()

def find_parm_value(fpv_list1, fpv_parm1):
    found1 = False
    for ix1, parm1 in enumerate(fpv_list1):
        if (parm1 == fpv_parm1):
            found1 = True
            fpv_str1 = fpv_list1[ix1+1]
            break
    if (found1 == False):
        fpv_str1 = ""
    return(fpv_str1)

def find_parm_value2(fpv_list1, fpv_parm1):
    found1 = False
    for ix1, parm1 in enumerate(fpv_list1):

##        print(" >>>", parm1[:len(fpv_parm1)], fpv_parm1)  # debug
##        if (ix1 > 20):              # debug
##            exit                    # debug

        if (parm1[:len(fpv_parm1)] == fpv_parm1):
            found1 = True
            fpv_str1 = fpv_list1[ix1][len(fpv_parm1):]
            break
    if (found1 == False):
        fpv_str1 = ""
    return(fpv_str1)

def find_parm_value3(fpv_str1, fpv_parm1, fpv_parm2):
    if (fpv_parm1 in fpv_str1):
        fpv_str2 = fpv_parm1
    elif (fpv_parm2 in fpv_str1):
        fpv_str2 = fpv_parm2
    else:
        fpv_str2 = ""
    return(fpv_str2)

def process_catalog_object(str_object, str_usercat):
    if (str_cluster == str_object[:len_cluster]) or (str_aix == str_object[:len_aix]):
        global n_obj
        n_obj += 1
        str_object = str_object.replace("--", "  ")
        str_object = str_object.replace("- ", "  ")
        str_object = str_object.replace(" -", "  ")

        # change parameters that do not fit the design

        str_object = str_object.replace("RECOVERY REQUIRED", "RECOVERY-REQUIRED")
        str_object = str_object.replace("RECOVERY TIMESTAMP LOCAL", "RECOVERY-TIMESTAMP-LOCAL")
        str_object = str_object.replace("RECOVERY TIMESTAMP GMT", "RECOVERY-TIMESTAMP-GMT")
        str_object = str_object.replace("DATA SET ENCRYPTION", "DATA-SET-ENCRYPTION")

        list1 = str_object.split()
        tmp_object = spc.join(list1)
        
        dsn1 = list1[1]
        list2 = dsn1.split(".")
        if (list2[0] == ("0" * 44)):
            hlq1 = ""
        else:
            hlq1 = list2[0]

        list_obj = []
        list_obj.append(dsn1)               # dsn
        list_obj.append(list1[0])           # object type
        list_obj.append(hlq1)               # hlq
        
        list_obj.append(find_parm_value(list1, lbl_storageclass))
        list_obj.append(find_parm_value(list1, lbl_managementclass))
        list_obj.append(find_parm_value(list1, lbl_dataclass))
        list_obj.append(find_parm_value2(list1, lbl_shroptns))
        list_obj.append(find_parm_value3(tmp_object, lbl_speed, lbl_recovery))
        list_obj.append(find_parm_value3(tmp_object, lbl_noerase, lbl_erase))
        list_obj.append(find_parm_value3(tmp_object, lbl_nonindexed, lbl_indexed))
        list_obj.append(find_parm_value3(tmp_object, lbl_noreuse, lbl_reuse))
        list_obj.append(find_parm_value3(tmp_object, lbl_nonspanned, lbl_spanned))
        list_obj.append(find_parm_value3(tmp_object, lbl_statistics, ""))
        list_obj.append(str_usercat)
        list_obj.append(find_parm_value(list1, lbl_volser))
        list_obj.append(find_parm_value(list1, lbl_space_type))
        list_obj.append(find_parm_value(list1, lbl_space_pri))
        list_obj.append(find_parm_value(list1, lbl_space_sec))
        list_obj.append(find_parm_value(list1, lbl_creation))
        list_obj.append(find_parm_value(list1, lbl_data))
        list_obj.append(find_parm_value(list1, lbl_index))
        list_obj.append(find_parm_value(list1, lbl_keylen))
        list_obj.append(find_parm_value(list1, lbl_rkp))
        list_obj.append(find_parm_value(list1, lbl_avglrecl))
        list_obj.append(find_parm_value(list1, lbl_maxlrecl))
        list_obj.append(find_parm_value(list1, lbl_cisize))
        list_obj.append(find_parm_value(list1, lbl_rec_total))
        list_obj.append(find_parm_value(list1, lbl_rec_deleted))
        list_obj.append(find_parm_value(list1, lbl_rec_inserted))
        list_obj.append(find_parm_value(list1, lbl_rec_updated))
        list_obj.append(find_parm_value(list1, lbl_rec_retrieved))
        list_obj.append(find_parm_value(list1, lbl_excps))
        list_obj.append(find_parm_value(list1, lbl_extents))
        list_obj.append(find_parm_value(list1, lbl_splits_ci))
        list_obj.append(find_parm_value(list1, lbl_splits_ca))
        list_obj.append(find_parm_value(list1, lbl_freespace_ci))
        list_obj.append(find_parm_value(list1, lbl_freespace_ca))
        list_obj.append(find_parm_value(list1, lbl_freespc))
        list_obj.append(find_parm_value(list1, lbl_hi_a_rba))
        list_obj.append(find_parm_value(list1, lbl_hi_u_rba))
        
        str_object = delim1.join(list_obj)
        write_line(file_output1, str_object)

    return()

global delim1
delim1 = ";"
delim2 = "-"
spc    = " "

page_header1 = "LISTING FROM CATALOG -- "
msg_prefix = "IDC"
len_msg_prefix = len(msg_prefix)
catalog_totals_line = spc * 8
len_cat_totals_line = len(catalog_totals_line)

str_cluster = "CLUSTER"
len_cluster = len(str_cluster)

str_aix     = "AIX"
len_aix     = len(str_aix)

# program defined variables

hdr_dsn                = "DSN"
hdr_object_type        = "OBJECT TYPE"
hdr_hlq                = "HLQ"

hdr_storageclass       = "STORCLAS"
lbl_storageclass       = "STORAGECLASS"
hdr_managementclass    = "MGMTCLAS"
lbl_managementclass    = "MANAGEMENTCLASS"
hdr_dataclass          = "DATACLAS"
lbl_dataclass          = "DATACLASS"

hdr_shroptns           = "SHROPTNS"
lbl_shroptns           = "SHROPTNS"
len_shroptns           = len(lbl_shroptns)

hdr_recovery_speed     = "RECOVERY SPEED"
lbl_recovery           = "RECOVERY"
lbl_speed              = "SPEED"

hdr_noerase_erase      = "NOERASE ERASE"
lbl_noerase            = "NOERASE"
lbl_erase              = "ERASE"

hdr_nonindexed_indexed = "NONINDEXED INDEXED"
lbl_nonindexed         = "NONINDEXED"
lbl_indexed            = "INDEXED"

hdr_noreuse_reuse      = "NOREUSE REUSE"
lbl_noreuse            = "NOREUSE"
lbl_reuse              = "REUSE"

hdr_nonspanned_spanned = "NONSPANNED SPANNED"
lbl_nonspanned         = "NONSPANNED"
lbl_spanned            = "SPANNED"

hdr_statistics         = "STATISTICS"
lbl_statistics         = "MAY BE INCORRECT"

hdr_catalog            = "CATALOG"
lbl_catalog            = "CATALOG"

hdr_volser             = "VOLSER"
lbl_volser             = "VOLSER"

hdr_space_type         = "SPACE TYPE"
lbl_space_type         = "SPACE-TYPE"
hdr_space_pri          = "SPACE PRI"
lbl_space_pri          = "SPACE-PRI"
hdr_space_sec          = "SPACE SEC"
lbl_space_sec          = "SPACE-SEC"

hdr_creation           = "CREATION"
lbl_creation           = "CREATION"

hdr_data               = "DATA"
lbl_data               = "DATA"
hdr_index              = "INDEX"
lbl_index              = "INDEX"

hdr_keylen             = "KEYLEN"
lbl_keylen             = "KEYLEN"
hdr_rkp                = "RKP"
lbl_rkp                = "RKP"

hdr_avglrecl           = "AVGLRECL"
lbl_avglrecl           = "AVGLRECL"
hdr_maxlrecl           = "MAXLRECL"
lbl_maxlrecl           = "MAXLRECL"
hdr_cisize             = "CISIZE"
lbl_cisize             = "CISIZE"

hdr_rec_total          = "REC TOTAL"
lbl_rec_total          = "REC-TOTAL"
hdr_rec_deleted        = "REC DELETED"
lbl_rec_deleted        = "REC-DELETED"
hdr_rec_inserted       = "REC INSERTED"
lbl_rec_inserted       = "REC-INSERTED"
hdr_rec_updated        = "REC UPDATED"
lbl_rec_updated        = "REC-UPDATED"
hdr_rec_retrieved      = "REC RETRIEVED"
lbl_rec_retrieved      = "REC-RETRIEVED"

hdr_excps              = "EXCPS"
lbl_excps              = "EXCPS"

hdr_extents            = "EXTENTS"
lbl_extents            = "EXTENTS"

hdr_splits_ci          = "SPLITS CI"
lbl_splits_ci          = "SPLITS-CI"
hdr_splits_ca          = "SPLITS CA"
lbl_splits_ca          = "SPLITS-CA"

hdr_freespace_ci       = "FREESPACE %CI"
lbl_freespace_ci       = "FREESPACE-%CI"
hdr_freespace_ca       = "FREESPACE %CA"
lbl_freespace_ca       = "FREESPACE-%CA"

hdr_freespc            = "FREESPC"
lbl_freespc            = "FREESPC"

hdr_hi_a_rba           = "HI A RBA"
lbl_hi_a_rba           = "HI-A-RBA"
hdr_hi_u_rba           = "HI U RBA"
lbl_hi_u_rba           = "HI-U-RBA"

# end of program defined variables

n_null = 0
n_hdr  = 0
n_obj  = 0

str_object = ""

file_output1 = open("zz_fileout_3tabulate_1objects.txt", "w")

list_obj = [hdr_dsn, hdr_object_type, hdr_hlq, hdr_storageclass, \
            hdr_managementclass, hdr_dataclass, hdr_shroptns, \
            hdr_recovery_speed, hdr_noerase_erase, hdr_nonindexed_indexed, \
            hdr_noreuse_reuse, hdr_nonspanned_spanned, hdr_statistics, \
            hdr_catalog, hdr_volser, hdr_space_type, hdr_space_pri, \
            hdr_space_sec, hdr_creation, hdr_data, hdr_index, hdr_keylen, \
            hdr_rkp, hdr_avglrecl, hdr_maxlrecl, hdr_cisize, hdr_rec_total, \
            hdr_rec_deleted, hdr_rec_inserted, hdr_rec_updated, \
            hdr_rec_retrieved, hdr_excps, hdr_extents, hdr_splits_ci, \
            hdr_splits_ca, hdr_freespace_ci, hdr_freespace_ca, hdr_freespc, \
            hdr_hi_a_rba, hdr_hi_u_rba]

str_object = delim1.join(list_obj)
write_line(file_output1, str_object)

file_output2 = open("zz_fileout_3tabulate_2messages.txt", "w")

with open("aa_idcams_listcat.txt", "r") as file_input1:
    for n_rec, line_input1 in enumerate(file_input1, start=0):
        line_input2 = line_input1.rstrip()      # remove newline

#       # mainline

        line_input2 = line_input2[1:]           # remove write control character

        if (len(line_input2) == 0):
            n_null += 1
            #write_line(file_output2, line_input2)   # for debugging
        elif(line_input2.find(page_header1) != -1):
            n_hdr += 1
            str_usercat = line_input2[53:]
            #write_line(file_output2, line_input2)   # for debugging
        elif(line_input2[:len_msg_prefix] == msg_prefix): # skip message lines
            pass
            #write_line(file_output2, line_input2)   # for debugging
        elif(line_input2[:len_cat_totals_line] == catalog_totals_line): # skip catalog totals lines
            pass
            #write_line(file_output2, line_input2)   # for debugging            
        else:
            if (line_input2[:1] == spc):            # continue to existing object
                str_object += (spc + line_input2)   # append line
            else:                                   # new catalog object
                process_catalog_object(str_object, str_usercat)
                str_object = line_input2

#       write_line(file_output1, obj_cat)

##                if (n_rec > 9999):
##                    break    
                    
#       # end of mainline                

process_catalog_object(str_object, str_usercat)      # process last object

file_output1.close()
file_output2.close()

print()
print("  >>> Number of input lines.....", n_rec)
print("  >>> Number of  null lines.....", n_null)
print("  >>> Number of page headers....", n_hdr)
print("  >>> Number of catalog objects.", n_obj)
print()
print("  >>> EOP")

exit()

############################################################################
