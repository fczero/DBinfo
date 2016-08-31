# -*- coding: utf-8 -*-

import sqlite3
import db_tables
import sys
import re

PARAM_COUNT       = db_tables.CP_MACRO_NAME.index('parameter_count')
STRUCT_KEY        = db_tables.CP_PARA_NAME.index('Struct_key')
STR_PARAM_COUNT   = 4
DB_MACRO_NAME_COL = len(db_tables.CP_MACRO_NAME)
NAME              = 0

DB_PATH       = '.\\'
CP_PARA_NAME  = DB_PATH + 'cp_para_name.db'
VER_INFO      = DB_PATH + 'VER_INFO.db'
VER_INFO_3G   = DB_PATH + '3G_VER_INFO.db'
CP_COMBO_NAME = DB_PATH + 'cp_combo_name.db'
CP_END_NAME   = DB_PATH + 'cp_end_name.db'
CP_MACRO_NAME = DB_PATH + 'cp_macro_name.db'
CP_STR_PTR    = DB_PATH + 'cp_str_ptr.db'
VER_INFO_LTE  = 'VER_INFO.db'
VER_INFO_3G   = '3G_VER_INFO.db'

def Get_Default_Value(limit_print_string):
    """ given a limit print string, returns the default value based on first number
    """
    m = re.match("\D*(\d*)", limit_print_string)
    return m.group(1)

def Get_Table_Value(table_name, index):
    table_name = 'db_tables.' + table_name
    table = eval(table_name)
    return (table[int(index)])

def Get_Parameter_Numbers_From_Indices(macro_no, parameter_indices_list, div=0):
    """given macro number, parameter list, and division returns list of parameter numbers
    """
    retVal = []
    for ctr, index in enumerate(parameter_indices_list):
        parameter_no = Get_Parameter_Number_From_Index(macro_no, parameter_indices_list[ctr], div)
        retVal.append(parameter_no)
    return retVal

def Get_Hex_Parameter_Count(key_no):
    """given key number returns hex parameter count
    """
    return  Get_Parameter_Attribute(key_no, 'hex_parameter_count')

def Get_Total_Hex_Parameter_Count(struct_key):
    """given struct key returns total hex parameter count
    """
    return  Get_Struct_Attribute(struct_key, 'total_hex_parameter_count')

def Get_Ascii_Parameter_Count(key_no):
    """given key number returns hex parameter count
    """
    return  Get_Parameter_Attribute(key_no, 'ascii_parameter_count')

def Get_Parameter_Repeat_Count(key_no):
    """given key number returns repeat count
    """
    return  Get_Parameter_Attribute(key_no, 'Repeat_count')

def Get_Parameter_Repeat_Flag(key_no):
    """given key number returns repeat count
    """
    return  Get_Parameter_Attribute(key_no, 'Repeat_flg')

def Get_Parameter_Input_Size(key_no):
    """given key number returns input size
    """
    return  Get_Parameter_Attribute(key_no, 'input_size')

def Get_Parameter_Display_Size(key_no):
    """given key number returns display size
    """
    return  Get_Parameter_Attribute(key_no, 'display_size')

def Get_Total_Ascii_Parameter_Count(struct_key):
    """given struct key returns total ascii parameter count
    """
    return  Get_Struct_Attribute(struct_key, 'total_ascii_parameter_cou')

def Get_Non_Struct_Parameters_Of_Struct(struct_key):
    parameters          = Get_Parameters_Of_Struct(struct_key)
    str_only_parameters = Get_Struct_Parameters_Of_Struct(struct_key)
    for  parameter in str_only_parameters:
        if parameter in parameters:
            parameters.remove(parameter)
    return parameters

def Get_Struct_Parameters_Of_Struct(struct_key):
    parameter_list = Get_Parameters_Of_Struct(struct_key)
    retVal         = []
    for parameter in parameter_list:
        if Get_Parameter_Attribute(parameter, 'Struct_key'):
            retVal.append(parameter)
    return retVal

def Get_Parameters_Of_Struct(struct_key):
    """ given struct key, returns list of parameters
    """
    struct_info     = getStrPtrInfo(struct_key)
    parameter_count = int(struct_info[db_tables.CP_STR_PTR.index('parameter_count')])
    lower_limit     = int(Get_Struct_Parameter_Index_Start())
    upper_limit     = lower_limit + parameter_count
    parameter_list  = struct_info[lower_limit:upper_limit]
    return list(parameter_list)

def Get_Struct_Parameter_Index_Start():
    return  db_tables.CP_STR_PTR.index('parameter_key_list1')

def Get_Struct_Parameters_Of_Macro(macro_number):
    """ given macro number, returns a list of struct parameters 
        format: [[div1 parameters], [div2 parameters], ...]
    """
    params_list =  Get_Parameters_Of_Macro(macro_number)
    retVal = []
    for div, paramList in enumerate(params_list):
        divList = []
        for param in paramList:
            if Get_Parameter_Attribute(param, 'Struct_key'):
                divList.append(param)
        retVal.append(divList)
    return retVal

def Get_Struct_Key_From_Parameter(key_no):
    return  Get_Parameter_Attribute(key_no, 'Struct_key')

def Get_Parameter_Name_From_Key(key_no):
    return  Get_Parameter_Attribute(key_no, 'parameter')

def Get_Struct_Name_From_Key(struct_key):
    return  Get_Struct_Attribute(struct_key, 'struct_name')

def Get_Struct_Ptr_Column_Count():
    return len(db_tables.CP_STR_PTR)

def Get_Parameter_Column_Count():
    return len(db_tables.CP_PARA_NAME)

def Get_Parameter_Column_Name(columnIndex):
    return  db_tables.CP_PARA_NAME[columnIndex]

def Get_Macro_Name(macro):
    """ given macro number, return the macro name as string
    """
    return Get_Macro_Attribute(macro, 'macro_name')

def Get_Macro_Attribute(macro, column, div=0):
    """ given parameter number and column name, returns value as string """
    info = getMacroInfo(str(macro))
    col = int(db_tables.CP_MACRO_NAME.index(column))
    return (info[div][col])

def Get_Parameter_Info_From_Index(macro, index, div=0):
    """ given macro, index, and division;
        return tuple of parameter info for that index.
    """
    info                 = getMacroInfo(str(macro))
    paramsAll            = getParamsAll(info)
    paramsInfoAll        = getParamsInfoAll(paramsAll)
    paramsInfoWithStrAll = insertStrParamsAll(paramsInfoAll)
    param_index          = db_tables.CP_PARA_NAME.index('key_no')
    matches              = [param for ctr, param in enumerate(paramsInfoWithStrAll[div])\
                           if ctr == index]
    return matches[0]

def Get_Parameter_Number_From_Index(macro, index, div=0):
    """ given macro, index, and division;
        return tuple of parameter info for that parameter index.
    """
    param_number = db_tables.CP_PARA_NAME.index('key_no')
    paramInfo    = Get_Parameter_Info_From_Index(macro,\
                                                index,\
                                                int(div))
    retVal       = paramInfo[param_number]
    return retVal

def Get_Parameter_Info_From_Name(macro, parameter_name, div=0):
    """ given macro, parameter name, and division;
        return tuple of parameter info for that parameter name.
        First match only
    """
    info                 = getMacroInfo(str(macro))
    paramsAll            = getParamsAll(info)
    paramsInfoAll        = getParamsInfoAll(paramsAll)
    paramsInfoWithStrAll = insertStrParamsAll(paramsInfoAll)
    param_index          = db_tables.CP_PARA_NAME.index('parameter')
    matches              = [param for param in paramsInfoWithStrAll[div] \
                           if param[param_index] == parameter_name]
    if matches:
        retVal = matches[0]
    else:
        retVal = ()
    return retVal

def Get_Parameter_Number_From_Name(macro, parameter_name, div=0):
    """ given macro, parameter name, and division;
        return parameter number.
        First match only
    """
    param_number = db_tables.CP_PARA_NAME.index('key_no')
    paramInfo    = Get_Parameter_Info_From_Name(macro,\
                                                parameter_name,\
                                                int(div))
    retVal       = paramInfo[param_number]
    return retVal

def Get_Last_Row_From_Table(db_name, table_name, column):
    """ given database name and column, returns last row from that table """
    db    = sqlite3.connect(db_name)
    c     = db.cursor()
    query = "select * from {table} where {col} = \
        (SELECT MAX({col}) FROM {table})".format(table=table_name, col=column)
    c.execute(query)
    info  = c.fetchone()
    print 'Last Entry:', info
    return info

def getVerDbFromRat(RAT_type):
    """ given RAT type returns the file name of the version database """
    if RAT_type == 'LTE':
        db_filename = VER_INFO_LTE
    else:
        db_filename = VER_INFO_3G
    return db_filename

def Get_MT_Version(RAT_type, db_path=DB_PATH):
    """ returns MTVER info from last version info row in database based on RAT type """
    filename = getVerDbFromRat(RAT_type)
    db_name = db_path + filename
    info = Get_Last_Row_From_Table(db_name, 'VER_INFO', 'NO')
    return info[db_tables.VER_INFO.index('MTVER')]

def Get_Scenario_Version(RAT_type, db_path=DB_PATH):
    """ returns VER info from last version info row  in database based on RAT type """
    filename = getVerDbFromRat(RAT_type)
    db_name = db_path + filename
    info = Get_Last_Row_From_Table(db_name, 'VER_INFO', 'NO')
    return info[db_tables.VER_INFO.index('VER')]

def getComboInfo(key, db_name=CP_COMBO_NAME):
    """ given macro number search combo name db returns the list of tuples of queries """
    db = sqlite3.connect(db_name)
    c = db.cursor()
    info = []
    for row in c.execute("select * from {} where macro_no =\
        {}".format('cp_combo_name', key)):
        info.append(row)
    db.close()
    return info

def Get_Combo_Box_Value_Attribute(key, comboIndex, column):
    """ given parameter number, combo index,  column name returns value as string """
    info = getComboInfo(key)
    col = int(db_tables.CP_COMBO_NAME.index(column))
    return (info[int(comboIndex)-1][col])

def getParaInfo(key, db_name=CP_PARA_NAME):
    """ given macro number search para name db returns tuple of queries """
    db = sqlite3.connect(db_name)
    c = db.cursor()
    c.execute("select * from {} where key_no = {}".format('cp_para_name', key))
    info = c.fetchone()
    db.close()
    return info

def getStrPtrInfo(struct_key, db_name=CP_STR_PTR):
    """ given struct key number search str ptr db, returns tuple of queries """
    db = sqlite3.connect(db_name)
    c = db.cursor()
    c.execute("select * from {} where struct_key = {}".format('cp_str_ptr', struct_key))
    info = c.fetchone()
    db.close()
    return info

def Get_Struct_Attribute(struct_key, column):
    """ given parameter number, column name returns value as string """
    info = getStrPtrInfo(struct_key)
    col = int(db_tables.CP_STR_PTR.index(column))
    return (info[col])

def Get_Struct_Attribute_From_Index(struct_key, columnIndex):
    """ given parameter number, column index returns value as string """
    info = getStrPtrInfo(struct_key)
    return (info[columnIndex])

def Get_Parameter_Attribute(key, column):
    """ given parameter number, column name returns value as string """
    info = getParaInfo(key)
    col = int(db_tables.CP_PARA_NAME.index(column))
    return (info[col])

def Get_Parameter_Attribute_From_Index(key, columnIndex):
    """ given parameter number, column index returns value as string """
    info = getParaInfo(key)
    return (info[columnIndex])

def getEndInfo(key, db_name):
    """ given macro number search end name db returns the list of tuple of queries """
    db = sqlite3.connect(db_name)
    c = db.cursor()
    info = []
    for row in c.execute("select * from {} where macro_no = {}".format('cp_end_name', key)):
        info.append(row)
    db.close()
    return info

def Get_Exit_Code_Attribute(key, price, db_path=DB_PATH):
    """ given macro number, parameter price returns value as string """
    if db_path == DB_PATH:
        db_name = CP_END_NAME
    else:
        db_name = db_path + 'cp_end_name.db'
    info = getEndInfo(key, db_name)
    for row in info:
        print row
        if row[db_tables.CP_END_NAME.index('parameter_price')] == float(price):
            return row[db_tables.CP_END_NAME.index('parameter_price_name')]

def getMacroInfo(key, db_name=CP_MACRO_NAME):
    """ given macro number search macro name db returns the list of tuples of queries """
    db = sqlite3.connect(db_name)
    c = db.cursor()
    info = []
    for row in c.execute("select * from {} where macro_no = {}".format('cp_macro_name', key)):
        info.append(row)
    db.close()
    return info

def getNumParams(row):
    """ returns int num of parameters """
    return (int(row[PARAM_COUNT]))

def getParamsAll(allMacroInfo):
    """ given list of tuples of queries returns list of list of parameters (list per result) """
    return map(getParams, allMacroInfo)

def getParams(macroInfo):
    """ given tuples of queries returns list of parameters (list per result) """
    retVal = []
    numOfParams = getNumParams(macroInfo)
    for index in range(1, numOfParams+1):
        retVal.append(macroInfo[PARAM_COUNT+index])
    return retVal

def getParamsInfoAll(allParamsList):
    """ given list within a list of parameters returns list within a list of tuples of parameters from para name db """
    return map(getParamsInfo, allParamsList)

def getParamsInfo(paramsList, db_name=CP_PARA_NAME):
    """ given list of parameters
        returns list of tuples of parameters from para name db
    """
    db = sqlite3.connect(db_name)
    c = db.cursor()
    retVal = []
    for param in paramsList:
#refactor for unicode support
        c.execute("select * from {} where key_no = {}".format(\
            'cp_para_name', str(param)))
        info = c.fetchone()
        retVal.append(info)
    db.close()
    return retVal

def insertStrParamsAll(allParamsInfo):
    """ given list within a list of tuples of parameters
        returns list within a list of tuples of parameters with struct parameters
        inserted after each struct
    """
    return map(insertStrParams, allParamsInfo)


def insertStrParams(paramsInfo):
    """ given list of tuples of parameters
        returns list of tuples of parameters with struct parameters
        inserted after each struct
    """
    retVal = []
#refactor to pythonic way; enumerate
    ctr = 0
    for param in paramsInfo[:]:
        #print param
        retVal.append(param)
        if param[STRUCT_KEY]:
            #print "---STRUCT"
            structParams = getStrParams(param[STRUCT_KEY])
            insertData = getParamsInfo(structParams)
            insertData = insertStrParams(insertData)
            for data in insertData:
                #print data
                retVal.append(data)
            #print "---End of STRUCT"
        ctr += 1

    for data in paramsInfo:
        pass
        #print data
    return retVal

def getStrParams(key, db_name=CP_STR_PTR):
    """ given struct key 
        returns list of parameters
    """
    db = sqlite3.connect(db_name)
    c = db.cursor()
    c.execute("select * from {} where struct_key = {}".format('cp_str_ptr', key))
    info = c.fetchone()
    db.close()
    retVal = []
    paramCount = info[STR_PARAM_COUNT]
    ctr = 0
    for value in info[STR_PARAM_COUNT+2:]:
        if value != 0.0:
            ctr += 1
            retVal.append(value)
    return retVal
    
def getStrParamCount(key, db_name=CP_STR_PTR):
    """ given struct key 
        returns integer count of parameters
    """
    db = sqlite3.connect(db_name)
    c = db.cursor()
    c.execute("select * from {} where struct_key = {}".format('cp_str_ptr', key))
    info = c.fetchone()
    db.close()
    if info:
        return int(info[STR_PARAM_COUNT])
    else:
        return 0
    
def table_columns(db_name):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    c.execute("select * from {}".format(db_name[:-3]))
    for i,v in enumerate(c.description):
        print i, v[0]
    db.close()

def Get_Parameters_Of_Macro(macro_number):
    """ given macro number, return the list of list of parameters
        format: [[div1 parameters], [div2 parameters], ...]
    """
    retVal = []
    info = getMacroInfo(str(macro_number))
    paramsAll = getParamsAll(info)
    paramsInfoAll = getParamsInfoAll(paramsAll)
    paramsInfoWithStrAll = insertStrParamsAll(paramsInfoAll)
    for div, params in enumerate(paramsInfoWithStrAll):
        divParams = []
        for info in params:
            divParams.append(info[db_tables.CP_PARA_NAME.index('key_no')])
        retVal.append(divParams)
    return retVal

def Remove_indices(paramsList, indices):
    pass
    
#######################################################
if __name__ == "__main__":
    """ given database name with extension
        prints table headers
    """
    if len(sys.argv) > 1:
        db_name = sys.argv[1]
    table_columns(db_name)

