import importlib
import json
import os
import re

from robot.api.deco import keyword

from Lib import SYSBase


def spider_case_and_data(script_path, script_type, case_name=('案例', 'case', 'Case'),
                         date_name=("数据", "data", "Data")) -> dict:
    """

    :param date_name:
    :param case_name:
    :param script_path: 扫描路径
    :param script_type: 目标文件后缀
    :return: 目标文件路径
    """
    final_case_files = {}
    final_data_files = {}
    for root, dirs, files in os.walk(script_path, topdown=False):
        for fi in files:
            dfile = os.path.join(root, fi)
            if dfile.endswith(script_type):
                for i in case_name:
                    if i in dfile:
                        final_case_files[fi] = dfile.replace("\\", "/")
                        # final_case_files.append(dfile.replace("\\", "/"))
                for j in date_name:
                    if j in dfile:
                        final_data_files[fi] = dfile.replace("\\", "/")
                        # final_data_files.append(dfile.replace("\\", "/"))
    return final_case_files, final_data_files


def spider(script_path, script_type):
    """

    :param script_path: 扫描路径
    :param script_type: 目标文件后缀
    :return: 目标文件路径
    """
    final_files = []
    for root, dirs, files in os.walk(script_path, topdown=False):
        for fi in files:
            dfile = os.path.join(root, fi)
            if dfile.endswith(script_type):
                final_files.append(dfile.replace("\\", "/"))
    return final_files


def scanner(files_list, cmd):
    """

    :param files_list: 扫描路径
    :param cmd: 待匹配正则表达式
    :return: 关键字与所在位置的映射关系
    """
    result_json = {}
    for item in files_list:
        fp = open(item, "r", encoding="utf-8")
        data = fp.readlines()
        for line in data:
            now_code = line.strip("\n")
            for unsafe in [cmd]:
                flag = re.findall(unsafe, now_code)
                if len(flag) != 0:
                    result_json[flag[0]] = item[len(os.getcwd().replace("\\", "/")) + 1:]
    if result_json is not None:
        return result_json


def read_file_to_json(path, encoding='utf-8'):
    """
    读取文件后转换为json格式返回
    :param path:读取文件地址
    :param encoding:编码格式
    :return:文件内容的json格式
    """
    with open(path, 'r', encoding=encoding) as file:
        file_content = file.read()
        file_content_json = json.loads(file_content)
        return file_content_json


def read_rfdata(path, rf_data, file_type='.json'):
    """

    :param path: rf_data扫描路径，指定为当前执行类同级目录
    :param rf_data: 目标文件名称
    :param file_type: 文件后缀类型
    :return: 文件json格式内容
    """
    data_path = ''
    for root, dirs, files in os.walk(path, topdown=False):
        for fi in files:
            dfile = os.path.join(root, fi)
            if dfile.endswith(file_type) and rf_data in dfile:
                data_path = dfile.replace("\\", "/")
    if data_path is not None:
        return read_file_to_json(data_path)
def replace_data(path,fun_name,rf_data):
    """


    :param path: 数据文件扫描路径，指定为当前执行类同级目录
    :param fun_name: 当前执行函数名称
    :param rf_data: 替换文件内容
    :return: req_data,rf_data和req_data合并后的内容
    """
    req_data = read_file_to_json(path+"\\"+fun_name+".json")

    req_data = replace_data_it(req_data,rf_data)

    print(req_data)
    # print(rf_data)  dict list tuple

    return fun_name

def replace_data_it(dict_a,dict_b):
    """
    以基础参数为模板，以b中的键在a中存在的，且值的类型相同的则替换对于的值
    dict_a ={"aa":"aa","cc":"cc"} dict_b ={"aa":"bb","dd":"dd"} => result_dict ={"aa":"bb","cc":"cc"}

    dict_a ={"aa":"aa","cc":{},"dd":{"ee":"ee"}} dict_b ={"aa":"aa","cc":{"zz":"zz"},"dd":{}} => result_dict ={"aa":"aa","cc":{"zz":"zz"},"dd":{}}

    dict_a ={"aa":"aa","cc":[{"dd":"dd"}],"ee":[]} dict_b ={"aa":"aa","cc":[],"ee":[{"zz":"zz"}]} => result_dict ={"aa":"aa","cc":[],"ee":[{"zz":"zz"}]} 值类型为list,tuple的，直接将dict_b的值替换进dict_a

    :param dict_a: 基础参数
    :param dict_b: 可变参数
    :return: 替换后的结果
    """
    dict_result = dict_a
    if type(dict_a) == dict:
        for item in dict_b.keys():
            if item in dict_a.keys():
                if type(dict_b[item]) == type(dict_a[item]):
                    if len(dict_b[item]) == len(dict_a[item]) or len(dict_b[item]) == 0 or len(dict_a[item]) ==0:
                        dict_a[item] = dict_b[item]
                    else:
                        dict_a[item] = replace_data_it(dict_a[item],dict_b[item])
    elif type(dict_a) == list:
        """
            暂不处理
        """
        dict_result = dict_b
    elif type(dict_a) == tuple:
        dict_result = dict_b
    else:
        pass
    return dict_result

def replace_data_list(dict_a,dict_b):
    dict_result = []
    for item in dict_b:
        if type(dict_a) == dict:
            for item in dict_b.keys():
                if item in dict_a.keys():
                    if type(dict_b[item]) == type(dict_a[item]):
                        if len(dict_b[item]) == len(dict_a[item]) or len(dict_b[item]) == 0 or len(dict_a[item]) == 0:
                            dict_a[item] = dict_b[item]
                        # elif len(dict_b[item]) == 0 or len(dict_a[item]) ==0:
                        #     dict_a[item] = dict_b[item]
                        else:
                            replace_data_it(dict_a[item], dict_b[item])
        elif type(dict_a) == list:
            """
                if len a>b : 以b长度为准 
                len a=b : 以b长度为准 
                len a<b : 以b长度为准 
            """
            replace_data_list(dict_a, dict_b)
        elif type(dict_a) == tuple:
            pass
        else:
            dict_a[item] = dict_b[item]


    pass
class SYSPublic(SYSBase):

    def __init__(self):
        SYSBase.__init__(self)
        self.restr = '@keyword\("(.*)"\)'
        self.paths = spider(os.getcwd(), ".py")
        self.fun_dict = scanner(self.paths, self.restr)
        self.case_name_dict, self.data_name_dict = spider_case_and_data(os.getcwd(), ".json")

    @keyword("通用执行案例")
    def execute_case(self, case_name) -> int:
        """

        :param case_name: 案例名称json文件名
        :return: 无
        """
        if case_name not in self.case_name_dict.keys():
            raise Exception("案例名称在当前项目下不存在，请检查！！！")
        case_content = read_file_to_json(self.case_name_dict[case_name], encoding='utf-8')
        case_content_step = dict(case_content).keys()

        # 循环执行步骤
        for step in case_content_step:
            if step[2:] not in self.fun_dict.keys():
                raise Exception("当前步骤注解{}在当前项目下不存在，请检查！！！".format(step[2:]))
            param = importlib.import_module(self.fun_dict[step[2:]][:-3].replace('/', '.'))
            my_object = getattr(param, self.fun_dict[step[2:]][:-3].split('/')[-1])
            my_class = my_object()
            attributes = [(name, getattr(my_object, name)) for name in dir(my_object)]
            for func in attributes:
                if hasattr(func[1], 'robot_name'):
                    if step[2:] == func[1].robot_name:
                        fun_name = func[0]
                        break

            my_func = getattr(my_class, fun_name)
            my_func(case_content[step]['rf_data'])
            # param_temp = param.keyword('打印函数')
            # print('123')

        # print(self.case_name_dict)

        # importlib.import_module('business.Demo01.SonDemo01')
        return case_name


if __name__ == '__main__':
    # read_file_to_json(r'D:\workspace\AutoTestFrame\Lib\business\Demo01\注册\案例\流程案例\注册成功.json', 'utf-8')

    # path = os.getcwd()
    # shell = '@keyword\((.*)\)'
    # ret = spider(path, ".py")
    # print(scanner(ret, shell))

    SYSPublic().execute_case("注册成功.json")

    # path = os.getcwd()

    # def scanDir(path):
    #     for i in os.listdir(path):
    #         file_d = os.path.join(path, i)
    #         if os.path.isdir(file_d):
    #             scanDir(file_d)
    #         else:
    #             print(file_d)

    # print("************")
    # scanDir(path)
    # print("************")
