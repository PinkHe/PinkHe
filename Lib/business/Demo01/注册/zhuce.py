import sys,os

from robot.api.deco import keyword

from Lib.SYSPublic import SYSPublic, read_file_to_json, read_rfdata, replace_data


# def read_rfdata(rf_data):
#     pass


class zhuce():
    @keyword("打印函数")
    def customization_print(self, msg):
        print(msg)

    @keyword("注册录入")
    def zhuceluru(self, rf_data,host_name=''):
        rf_data = read_rfdata(os.path.dirname(__file__)+"\\data",rf_data)
        req_data = replace_data(os.path.dirname(__file__)+"\\"+self.__class__.__name__+"_data",sys._getframe().f_code.co_name,rf_data)
        print(req_data)

    @keyword("注册返回")
    def zhucefanhui(self, rf_data):
        print(rf_data)


if __name__ == '__main__':
    zhuce().zhuceluru("注册录入.json")
