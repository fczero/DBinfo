# -*- coding: utf-8 -*-

from db_helper import *
import sys

def printInfo(paramsAll):
    for div, paramInfo in enumerate(paramsAll):
        print 'Detailed Division: %s' % (div+1)
        print '================='
        print 'Param_no, param_type, select_param_count, display_param_count, #struct_elements, param_limit, ascii_val, hex_val, param_name'
        count = 0
        param_type = 0
        struct_key = 0
        strParamCount = 0
        indentLevel = 0
        strStack = []
        for param in paramInfo:
            count += 1
            param_type = int(param[db_tables.CP_PARA_NAME.index('parameter_type')])
#refactor for unicode support
            param_limit = param[db_tables.CP_PARA_NAME.index('limit_print_string')]
            hex_val = int(param[db_tables.CP_PARA_NAME.index('hex_parameter_count')])
            ascii_val = int(param[db_tables.CP_PARA_NAME.index('ascii_parameter_count')])
            repeat_count = int(param[db_tables.CP_PARA_NAME.index('Repeat_count')])
            struct_key = int(param[db_tables.CP_PARA_NAME.index('Struct_key')])
            select_param_count = int(param[db_tables.CP_PARA_NAME.index('select_parameter_count')])
            display_param_count = int(param[db_tables.CP_PARA_NAME.index('display_parameter_count')])
            print '{:02}'.format(count, end=""),
            for i in range(0, indentLevel+1):
                print '|--',
            if 1:
                print u'{:4}\t\t{:>2} {:>2} {:>2} {:>2} {:>20} {:>6} {:>6} {:<40} '.format(int(param[0]),\
                                        param_type,\
                                        select_param_count,\
                                        display_param_count,\
                                        getStrParamCount(struct_key),\
                                        param_limit,\
                                        ascii_val,\
                                        hex_val,\
                                        param[3])

            else:
#refactor for unicode support
#console bug
#output to text is okay
                #print '{:4} '.format(int(param[0])),
                test = param[3]
#.encode produces bytes
#.decode produces unicode
                uni_test = test.encode('utf-8')
                print u'{:<40} '.format(test),
                print ''

            if param_type == db_tables.DATA_TYPES.index('struct'):
                indentLevel += 1
                if strParamCount:
                    strParamCount -= 1
                    strStack.append(strParamCount)
                strParamCount = getStrParamCount(struct_key)
            else:
                if strParamCount:
                    strParamCount -= 1
                    if not strParamCount:
                        indentLevel -= 1
                        if strStack:
                            strParamCount = strStack.pop()
                            if not strParamCount:
                                indentLevel -= 1




#######################################################
if __name__ == "__main__":
    api = '0'
    detail = '0'
    if len(sys.argv) > 1:
        api = sys.argv[1]
    if len(sys.argv) > 2:
        detail = sys.argv[2]
#test
    info = getMacroInfo(str(api))
    paramsAll = getParamsAll(info)
    paramsInfoAll = getParamsInfoAll(paramsAll)
    paramsInfoWithStrAll = insertStrParamsAll(paramsInfoAll)
#    for index,info in enumerate(paramsInfoWithStrAll):
#        print index, info
    print 'API: %s' % api
    if detail == '0':
        print 'Detail Level: Basic'
        printInfo(paramsInfoAll)
    else:
        print 'Detail Level: Advanced'
        printInfo(paramsInfoWithStrAll)

    #table_columns('cp_macro_name.db')
    #table_columns('cp_para_name.db')
    

