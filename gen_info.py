from db_helper import *
import sys

def printConvertInfo(oldParamsAll, oldMacroInfo,\
                     new_api=0,\
                     new_name='UPDATE_ME',\
                     new_param_count=0,\
                     newParamsAll={}):
    old_api = oldMacroInfo[0][db_tables.CP_MACRO_NAME.index('macro_no')]
    old_param_count = \
        oldMacroInfo[0][db_tables.CP_MACRO_NAME.index('parameter_count')]
    if not new_param_count:
        new_param_count = int(old_param_count)
    if not newParamsAll:
        newParamsAll = oldParamsAll
    header = '''
[Version]
Old=Version 6.00 LTE
New=Version 7.00 LTE

[Max Parameter Count]
Old=120
New=120

[Digit of Parameter Size]
Old=6
New=6

[Conversion Macro]
Macro Count=1
Old Macro No=2202,1
    '''
    print header

    for div, paramInfo in enumerate(oldParamsAll):
        count = 0
        print ";=============== %d to %s ===============" % (old_api, new_api)
        print "[Old%d_%s]" % (old_api, div+1)
        print "New Macro No=%s,%s" %(new_api, div+1)
        print "New Macro Name=%s" % new_name
        print "Reception Result Change=0"
        print "Execution Result Change=0"
        print "Exit Code Change=0"
        print "Macro Type Change=0"
        print "New Parameter Count=%d" % new_param_count
        print ""
        for param in paramInfo:
            count += 1
            elemParamType =\
                int(param[db_tables.CP_PARA_NAME.index('parameter_type')])
            repeatCount = \
                int(param[db_tables.CP_PARA_NAME.index('Repeat_count')])
            struct_key = int(param[db_tables.CP_PARA_NAME.index('Struct_key')])
            structParamCount = getStrParamCount(struct_key)
            elemParamName =\
                param[db_tables.CP_PARA_NAME.index('parameter')]
            elemParamNo =\
                int(param[db_tables.CP_PARA_NAME.index('key_no')])
            print ";== [%d] %s ===" % (elemParamNo, elemParamName)
            print "[Old%d_%s_PARA_%02d]" % (old_api, div+1, count)
            print "Element Parameter Type=%d" % elemParamType
            print "Repeat Count=%d" % repeatCount
            print "Struct Parameter Count=%d" % structParamCount
            print ""
        count = 0
        for param in newParamsAll[div]:
            count += 1
            upper = \
                int(param[db_tables.CP_PARA_NAME.index('parameter_upper1')])
            lower = \
                int(param[db_tables.CP_PARA_NAME.index('parameter_lower1')])
            paramType = \
                int(param[db_tables.CP_PARA_NAME.index('parameter_type')])
            asciiCount = \
                int(param[db_tables.CP_PARA_NAME.index('ascii_parameter_count')])
            hexCount = \
                int(param[db_tables.CP_PARA_NAME.index('hex_parameter_count')])
            defaultNum = \
                int(param[db_tables.CP_PARA_NAME.index('default_number')])
            elemParamType = \
                int(param[db_tables.CP_PARA_NAME.index('valiable_size')])
            repeatCount = \
                int(param[db_tables.CP_PARA_NAME.index('Repeat_count')])
            struct_key = int(param[db_tables.CP_PARA_NAME.index('Struct_key')])
            structParamCount = getStrParamCount(struct_key)
            elemParamName =\
                param[db_tables.CP_PARA_NAME.index('parameter')]
            elemParamNo =\
                int(param[db_tables.CP_PARA_NAME.index('key_no')])
            print ";== [%d] %s ===" % (elemParamNo, elemParamName)
            print "[New%d_%s_PARA_%02d]" % (new_api, div+1, count)
            # this is inverted in code
            print "Parameter Upper, Lower=%s,%s" % (lower, upper)

            print "Parameter Type=%d" % paramType
            print "Ascii Parameter Count=%d" % asciiCount
            print "Hex Parameter Count=%d" % hexCount
            print "Default Number=%d" % defaultNum
            print "Element Parameter Type=%d" % elemParamType
            print "Repeat Count=%d"  % repeatCount
            print "Struct Parameter Count=%d" % structParamCount
            print "Old Parameter Order=%d" % count
            print "Copy Pattern No=%d" % 1
            print ""

#######################################################
if __name__ == "__main__":
    old_api = '0'
    detail = '0'
    new_api = '0'
    if len(sys.argv) > 1:
        old_api = sys.argv[1]
    if len(sys.argv) > 2:
        new_api = sys.argv[2]
    old_info = getMacroInfo(str(old_api))
    old_paramsAll = getParamsAll(old_info)
    old_paramsInfoAll = getParamsInfoAll(old_paramsAll)
    old_paramsInfoWithStrAll = insertStrParamsAll(old_paramsInfoAll)

    new_info = getMacroInfo(str(new_api))
    new_paramsAll = getParamsAll(new_info)
    new_paramsInfoAll = getParamsInfoAll(new_paramsAll)
    new_paramsInfoWithStrAll = insertStrParamsAll(new_paramsInfoAll)
    printConvertInfo(old_paramsInfoWithStrAll, old_info,\
                     int(new_api),\
                     'PDSCH Broadcast Information Transmission Macro 2',\
                     15,\
                     new_paramsInfoWithStrAll)

    #table_columns('cp_macro_name.db')
    #table_columns('cp_para_name.db')
