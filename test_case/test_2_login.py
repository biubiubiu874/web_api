# 对 requests 发送请求封装成类：
# #
# # 1， 支持 session 管理（可以定义 session 属性）
# # 2，封装 visit 方法（可以发送 get 和 post 请求）
import json

from common.excel_handler import Excel
from common.loggin_handler import LoggingHandler
from common.request_handler import HTTPrequests
import unittest

from common.yaml_handler import yaml_read
from libs import ddt
from config import config

excel = Excel(config.config.data_path,1)
text_data = excel.read_cell_values()

@ddt.ddt
class Test_2(unittest.TestCase):
    def setUp(self):
        self.requests2 = HTTPrequests()
        self.log_config=yaml_read(r'C:\Users\41497\Desktop\面试\0207测试框架搭建\test\config\yaml.yaml')
        self.loggin=LoggingHandler(self.log_config['logger']['name'],self.log_config['logger']['file'])

    def tearDown(self):
        self.requests2.session.close()


    @ddt.data(*text_data)
    def test_requests(self,text_data):
        try:
            a = text_data['json']
            self.response2=self.requests2.visit(method='post',url=str(config.config.host+text_data['url']),json=eval(text_data['json']),headers=eval(text_data['headers']))
            expect=text_data['expected']

            self.assertEqual(expect,self.response2.json()['code'])



        except AssertionError as e:

            self.loggin.play_logger(e, 'ERROR')
            raise e