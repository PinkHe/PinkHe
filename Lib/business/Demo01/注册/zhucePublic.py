from robot.api.deco import keyword


class SonDemo01Public:
    @keyword("打印函数public")
    def Customization_print_public(self,msg):

        print(msg)


