# -*- coding: utf-8 -*-

import db_helper
import db_tables
import sys

def fixRepeatCount(repeatCount):
    """ returns 1 if repeatCount is 0, otherwise returns the original value.
        This is due to division by zero error on mail notification conversion.
    """
    #refactor me
    retVal = 0;
    if int(repeatCount):
        retVal = repeatCount
    else:
        retVal = 1
    return retVal


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
    #refactor this mess    
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
Macro Count=1'''
    print header
    print 'Old Macro No=%d,1' % old_api
    print ""

    for div, paramInfo in enumerate(oldParamsAll):
        #using count is non-pythonic
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
            #using count is non-pythonic
            count += 1
            elemParamType =\
                int(param[db_tables.CP_PARA_NAME.index('parameter_type')])
            repeatCount = \
                int(param[db_tables.CP_PARA_NAME.index('Repeat_count')])
            #fix repeatCount, refactor me
            repeatCount = fixRepeatCount(repeatCount)
            struct_key = int(param[db_tables.CP_PARA_NAME.index('Struct_key')])
            structParamCount = db_helper.getStrParamCount(struct_key)
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
        #using count is non-pythonic    
        count = 0
        for param in newParamsAll[div]:
            #using count is non-pythonic
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
            #fix repeatCount, refactor me
            repeatCount = fixRepeatCount(repeatCount)
            struct_key = int(param[db_tables.CP_PARA_NAME.index('Struct_key')])
            structParamCount = db_helper.getStrParamCount(struct_key)
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
    old_macro = '0'
    detail  = '0'
    new_macro = '0'
    if len(sys.argv) > 1:
        old_macro = sys.argv[1]
    if len(sys.argv) > 2:
        new_macro = sys.argv[2]
    old_info                 = db_helper.getMacroInfo(str(old_macro))
    old_paramsAll            = db_helper.getParamsAll(old_info)
    old_paramsInfoAll        = db_helper.getParamsInfoAll(old_paramsAll)
    old_paramsInfoWithStrAll = db_helper.insertStrParamsAll(old_paramsInfoAll)
    new_info                 = db_helper.getMacroInfo(str(new_macro))
    new_paramsAll            = db_helper.getParamsAll(new_info)
    new_paramsInfoAll        = db_helper.getParamsInfoAll(new_paramsAll)
    new_paramsInfoWithStrAll = db_helper.insertStrParamsAll(new_paramsInfoAll)
    new_macro_name           = db_helper.Get_Macro_Name(str(new_macro))
    new_macro_param_count    = db_helper.Get_Number_Of_Parameters_Of_Macro(str(new_macro))
    printConvertInfo(old_paramsInfoWithStrAll, old_info,\
                     int(new_macro),\
                     new_macro_name,\
                     new_macro_param_count,\
                     new_paramsInfoWithStrAll)
