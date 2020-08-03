#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/4 15:47
from test_tinyshop_keys.common.utility import common_utility
from selenium import webdriver
from test_tinyshop_keys.action.do_test import reflectmans

class test_neirong():

    def test_beegin(self,file):
        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        test_list = common_utility().get_csvs(file)
        for i in range(len(test_list)):
            try:
                for j in test_list[i]:
                    ele2 = j.strip("\n").split(',')
                    try:
                        if ele2[3] != '':
                            global yonglibiaoti
                            yonglibiaoti = ele2[3]
                            print("正在执行用例:"+yonglibiaoti)
                        if ele2[4] != '':
                            global yonglibianhao
                            yonglibianhao = ele2[4]
                        if ele2[5] != '':
                            global mokuai
                            mokuai = ele2[5]
                        runman = getattr(reflectmans, ele2[0])
                        runman(driver, j.strip("\n"))
                    except IndexError as inde:
                        pass
                    except AttributeError as a:
                        pass
            except Exception as e:
                print("-----此用例执行失败,详情查看测试报告或数据库中的错误信息-----")
                files = common_utility.get_erroe_img(driver)  # 截图
                common_utility.insert_data(
                    '1.0.1', mokuai, '功能测试', yonglibianhao, yonglibiaoti, '失败', e, files)
            else:
                print("--------------------此用例执行成功----------------------")
                common_utility.insert_data(
                    '1.0.1', mokuai, '功能测试', yonglibianhao, yonglibiaoti, '成功', '无', '无')