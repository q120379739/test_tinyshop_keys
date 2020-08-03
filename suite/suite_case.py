#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/10/21 17:38
#框架运行主入口

import time
from test_tinyshop_keys.case.neirong_text import test_neirong
from test_tinyshop_keys.common.utility import common_utility

class suite_tests():
    def __init__(self):
        moban_html = common_utility.get_config('ci', 'moban_html')
        new_html = common_utility.get_config('ci', 'new_html')
        test_csv = common_utility.get_config('ci', 'test_csv')
        self.moban_html = moban_html
        #HTML模板地址
        self.new_html = new_html
        #新HTML模板存放地址
        self.test_csv = test_csv
        #测试脚本地址

    def suite_test(self):
        test_neirong().test_beegin(self.test_csv)
        time.sleep(1)
        common_utility.write_html("1.0.1",self.moban_html,self.new_html)

if __name__ == '__main__':
    run = suite_tests()
    run.suite_test()
