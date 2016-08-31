# -*- coding: utf-8 -*-
import unittest
import db_helper
import db_tables


class TestDbHelper(unittest.TestCase):

    def setUp(self):
        self.api           = 2389
        self.info          = db_helper.getMacroInfo(str(self.api))
        self.paramsAll     = db_helper.getParamsAll(self.info)
        self.paramsInfoAll = db_helper.getParamsInfoAll(self.paramsAll)
        self.testData      = (2327,9002,2328,5204,5205,5206,2329,2330,2331,\
            2332,2333,2334,2335,2336,2337,2338,2339,2729,2340,2341,2730,\
            2342,2343,2731,2344,2345,2346,5126,5127,5128,5129,2347,2348,\
            2732,2349,4044,4045,4046,5130,2733,2350,2351,2352,2353,2354,\
            2355,2356,2357,5131,5132,2358,5111,5112,9003,2734,2735,5228,\
            5229,5230,5231,5207,2359,9084,2360,2316,2317,2318,2319,2320,\
            2321,2322,2323,2927,2928,2736,9002,2737,2738,2739,2740,2325,\
            9002,2326,2309,5133,2311,9002,2313,2314,2315,5134,5135,9002,\
            5136,5137,5138,9002)
        self.paramsInfoWithStrAll = db_helper.insertStrParamsAll(self.paramsInfoAll)

    def test_get_macro_info(self):
        self.assertEqual(self.info[0][db_helper.NAME], float(self.api))
        self.assertEqual(len(self.info[0]), db_helper.DB_MACRO_NAME_COL)
        self.assertEqual(len(self.info),2)
#        for index, param in enumerate(self.info):
#            print index, param

    def test_get_number_of_params(self):
        self.assertEqual(db_helper.getNumParams(self.info[0]), \
            int(self.info[0][db_helper.PARAM_COUNT]))
        self.assertEqual(db_helper.getNumParams(self.info[1]), \
            int(self.info[1][db_helper.PARAM_COUNT]))

    def test_get_params_list(self):
        self.assertEqual(len(self.paramsAll[0]), int(self.info[0][db_helper.PARAM_COUNT]))
        index = db_helper.PARAM_COUNT
        for param in self.paramsAll[0]:
            index += 1
            self.assertEqual(param, self.info[0][index])
#        for index, param in enumerate(self.paramsAll):
#            print index, param

    def test_get_param_info_from_list(self):
        self.assertEqual(len(self.paramsAll[0]), len(self.paramsInfoAll[0]))
        for index in range(0, len(self.paramsAll[0])):
            self.assertEqual(self.paramsAll[0][index], self.paramsInfoAll[0][index][0])

    def test_insert_struct_params(self):
        self.assertEqual(len(self.paramsInfoWithStrAll[0]), len(self.testData))
        for index in range(0, len(self.paramsInfoWithStrAll)):
            self.assertEqual(self.paramsInfoWithStrAll[0][index][0], self.testData[index])

    def test_combo_info(self):
        info = db_helper.getComboInfo(1017)
        self.assertEqual(len(info),3)
        names = ['SDM side not specified',\
                 'SDM (side A) specified',\
                 'SDM (side B) specified']
        for index in range(3):
            self.assertEqual(info[index][db_tables.CP_COMBO_NAME.index('macro_no')],1017)
            self.assertEqual(info[index][db_tables.CP_COMBO_NAME.index('parameter_price')],index)
            self.assertEqual(info[index][db_tables.CP_COMBO_NAME.index('parameter_price_name')],names[index])
    
    def test_paraminfo_from_name(self):
        test_data = (5310.0, 0.0, 0.0, u'Number of Message data', 65535.0,\
                     0.0, -1.0, 0.0, -1.0, 0.0, -1.0, 0.0, -1.0, 0.0,\
                     u'1 .. 32', 1.0, 9.0, 13.0, 4.0, 0.0, 0.0, 0.0, 1.0,\
                     1.0, 0.0, 0.0, 0.0, 0.0)
        parameter_name         = 'Number of Message data'
        macro                  = 2204
        actual                 = db_helper.Get_Parameter_Info_From_Name(macro, parameter_name)
        self.assertTupleEqual(actual, test_data)
        invalid_parameter_name = 'Invalid data'
        actual_invalid         = db_helper.Get_Parameter_Info_From_Name(macro, invalid_parameter_name)
        self.assertTupleEqual(actual_invalid, ())

    def test_paramNumber_from_name(self):
        test_data      =  (5310.0, 0.0, 0.0, u'Number of Message data', 65535.0,\
                          0.0, -1.0, 0.0, -1.0, 0.0, -1.0, 0.0, -1.0, 0.0,\
                          u'1 .. 32', 1.0, 9.0, 13.0, 4.0, 0.0, 0.0, 0.0, 1.0,\
                          1.0, 0.0, 0.0, 0.0, 0.0)
        parameter_name = 'Number of Message data'
        param_number   = db_tables.CP_PARA_NAME.index('key_no')
        macro          = 2204
        actual         = db_helper.Get_Parameter_Number_From_Name(macro, parameter_name)
        self.assertEqual(actual, test_data[param_number])

    def test_get_parameters_of_macro(self):
        macro_number = 1240
        div1         = [1808, 1142, 1809, 1810, 1138, 1139, 1140, 1141, 1144, 1145, 1146]
        test_data    = [div1]
        parameters   = db_helper.Get_Parameters_Of_Macro(1240)
        for index in range(len(test_data)):
            self.assertListEqual(parameters[index], test_data[index])

    def test_get_struct_parameters_of_macro(self):
        macro_number = 1240
        div1         = [1142]
        test_data    = [div1]
        parameters   = db_helper.Get_Struct_Parameters_Of_Macro(macro_number)
        for index in range(len(test_data)):
            self.assertListEqual(parameters[index], test_data[index])

    def test_get_struct_attribute(self):
        struct_key      = 1001
        name            = db_helper.Get_Struct_Attribute(struct_key, 'struct_name')
        hex_count       = db_helper.Get_Struct_Attribute(struct_key, 'total_hex_parameter_count')
        parameter_count = db_helper.Get_Struct_Attribute_From_Index(struct_key, 4)
        self.assertEqual(name, 'Equipment Component Info')
        self.assertEqual(hex_count, 4)
        self.assertEqual(parameter_count, 1.0)

    def test_struct_para_count(self):
        struct_key          = 2015
        test_data           = [2362, 2363, 2364]
        test_data_non_str   = [2362, 2363]
        test_data_str_only  = [2364]
        str_para_count      = db_helper.Get_Struct_Attribute(struct_key, 'str_para_count')
        self.assertEqual(str_para_count, 1)
        str_params_list     = db_helper.Get_Parameters_Of_Struct(struct_key)
        self.assertListEqual(str_params_list, test_data)
        str_only_params     = db_helper.Get_Struct_Parameters_Of_Struct(struct_key)
        self.assertListEqual(str_only_params, test_data_str_only)
        non_str_only_params = db_helper.Get_Non_Struct_Parameters_Of_Struct(struct_key)
        self.assertListEqual(non_str_only_params, test_data_non_str)

    def test_para_number_from_index(self):
        macro_no              = 1247
        index                 = 7
        div                   = 0
        actual_parameter_no = db_helper.Get_Parameter_Number_From_Index(macro_no, index)
        self.assertEqual(actual_parameter_no, 5327)
        indices               = [7, 8]
        actual_parameter_list = db_helper.Get_Parameter_Numbers_From_Indices(macro_no, indices)
        self.assertListEqual(actual_parameter_list, [5327, 5328])

    def test_get_default_value(self):
        string_list = ["32, 64, 128, 256, 512",
                       "0 .. 255",
                       "1, 2, 4, 6, 8, 10, 12, 14, 16, 32, 64, 128, 256",
                       "0 .. 1023",
                       "1 .. 16",
                       "0 .. 1",
                       "1 .. 64",
                       "API ID 1352"]
        expected_list = ["32",
                         "0",
                         "1",
                         "0",
                         "1",
                         "0",
                         "1",
                         "1352"]
        actual_list = []
        for limit in string_list:
            actual_list.append(db_helper.Get_Default_Value(limit))
        self.assertListEqual(actual_list, expected_list)

    def test_get_default_value_jap(self):
        string_list = ["32, 64, 128, 256, 512",
                       "0 .. 255",
                       "1, 2, 4, 6, 8, 10, 12, 14, 16, 32, 64, 128, 256",
                       "0 .. 1023",
                       "1 .. 16",
                       "0 .. 1",
                       "1 .. 64",
                       "本マクロ番号　1359"]
        expected_list = ["32",
                         "0",
                         "1",
                         "0",
                         "1",
                         "0",
                         "1",
                         "1359"]
        actual_list = []
        for limit in string_list:
            actual_list.append(db_helper.Get_Default_Value(limit))
        self.assertListEqual(actual_list, expected_list)

    def test_get_macro_name(self):
        expected_name = "Message Queue Setting"
        macro_number = '1004'
        actual_name = db_helper.Get_Macro_Name(macro_number)
        self.assertEqual(actual_name, expected_name)
        
if __name__ == "__main__":
    unittest.main()
