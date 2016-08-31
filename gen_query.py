from db_helper import *
import sys

def printQuery(paramsAll):
    count = 0
    for div, paramInfo in enumerate(paramsAll):
        print "--Detailed Division: %s" % (div+1)
        print "--================="
        for param in paramInfo:
            if count:
                print 'union all'
            key_no = int(param[db_tables.CP_PARA_NAME.index('key_no')])
            print initial(key_no)
            count += 1


def initial(key_no):
    ''' 
        given key_no as int
        returns query prefix as string 
    '''
    return 'select * from cp_para_name.cp_para_name where key_no = {}'.format(key_no)


#######################################################
if __name__ == "__main__":
    api = '0'
    detail = '0'
    if len(sys.argv) > 1:
        api = sys.argv[1]

    info = getMacroInfo(str(api))
    paramsAll = getParamsAll(info)
    paramsInfoAll = getParamsInfoAll(paramsAll)
    paramsInfoWithStrAll = insertStrParamsAll(paramsInfoAll)

    print "--API: %s" % api
    print "--Detail Level: Advanced"
    printQuery(paramsInfoWithStrAll)
