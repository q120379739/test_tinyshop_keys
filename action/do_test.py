#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/4 11:15
from test_tinyshop_keys.common.utility import common_utility
import time,pymysql


class reflectmans():

    @classmethod
    def goto(cls,driver,cmd):
        #跳转到
        driver.get(cmd.split(',')[1])
        print("跳转到:",cmd.split(',')[1])

    @classmethod
    def input(cls,driver,cmd):
        #send,输入
        if 'xpath' in cmd:
            choise = cmd.split(',')[1][6:]
            driver.find_element('xpath',choise).send_keys(cmd.split(',')[2])
            print("定位元素为:",choise,"输入:",cmd.split(',')[2])
        else:
            choise = cmd.split(',')[1][3:]
            driver.find_element('id',choise).send_keys(cmd.split(',')[2])
            print("定位元素为:",choise,"输入:",cmd.split(',')[2])

    @classmethod
    def singleclick(cls,driver,cmd):
        #点击
        if 'xpath' in cmd:
            choise = cmd.split(',')[1][6:]
            driver.find_element('xpath',choise).click()
            print("点击元素:",choise)
        else:
            choise = cmd.split(',')[1][3:]
            driver.find_element('id',choise).click()
            print("点击元素:",choise)

    @classmethod
    def delay(cls,driver,cmd):
        #等待
        thetime = cmd.split(',')[2]
        time.sleep(int(thetime))
        print('等待成功,等待时间为:',thetime)

    @classmethod
    def checklen(cls,driver,cmd):
        #检查text长度
        if 'xpath' in cmd:
            choise = cmd.split(',')[1][6:]
            ele = driver.find_element('xpath',choise).text
            if len(ele) != int(cmd.split(',')[2]):
                driver.find_element('xpath','元素长度不相等')#此行代码会抛出异常,以做用例断言
            else:
                print('长度检查成功,检查的长度为:', cmd.split(',')[2], '实际长度为', len(ele))
        else:
            choise = cmd.split(',')[1][3:]
            ele = driver.find_element('id',choise).text
            if len(ele) != int(cmd.split(',')[2]):
                driver.find_element('css selector','元素长度不相等')

            else:
                print('长度检查成功,检查的长度为:', cmd.split(',')[2], '实际长度为', len(ele))

    @classmethod
    def checktext(cls,driver,cmd):
        #检查text信息
        if 'xpath' in cmd:
            choice = cmd.split(',')[1][6:]
            ele = driver.find_element('xpath',choice).text
            if cmd.split(',')[2] != ele:
                driver.find_element('xpath','元素text数据不相等')#此行代码会抛出异常,以做用例断言
            else:
                print('检测完成',cmd.split(',')[2],'元素text相同')
        else:
            choice = cmd.split(',')[1][3:]
            ele = driver.find_element('id', choice).text
            if cmd.split(',')[2] != ele:
                driver.find_element('css selector','元素text数据不相等')#此行代码会抛出异常,以做用例断言
            else:
                print('检测完成',cmd.split(',')[2],'元素text相同')

    @classmethod
    def tab_window(cls,driver,cmd):
        #切换新打开的窗口
        windows = driver.window_handles
        driver.switch_to.window(windows[1])

    @classmethod
    def close_window(cls,driver,cmd):
        #关闭当前窗口
        driver.close()

    @classmethod
    def qiejin(cls,driver,cmd):
        # selenium切进frame域
        choice = cmd.split(',')[1][6:]
        driver.switch_to.frame(driver.find_element('xpath',choice))
        print("进入frame域")

    @classmethod
    def qiechu(cls,driver,cmd):
        #切出frame域到主域
        driver.switch_to.default_content()
        print("返回到主域")

    @classmethod
    def select(cls,driver,cmd):
        #cmd[1]为SQL语句,向数据库中查找数据
        sql_addr =common_utility.get_config('server_db','sql_addr')
        sql_user =common_utility.get_config('server_db','sql_user')
        sql_psword =common_utility.get_config('server_db','sql_psword')
        sql_database =common_utility.get_config('server_db','sql_database')
        conn = pymysql.connect(host=sql_addr, user=sql_user, passwd=sql_psword, database=sql_database, charset='utf8')
        cursor = conn.cursor()
        sql = cmd.split(',')[1]
        print("正在SQL语句:",sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        ele2 = []
        for i in result:
            for j in i:
                ele2.append(str(j))
        if cmd.split(',')[2] in ele2:
            print("数据库查询成功,数据相符")
        else:
            driver.find_element('xpath', '数据库内查无此数据')#此行代码会抛出异常,以做用例断言

    @classmethod
    def queding(cls,driver,cmd):
        #处理确定弹窗
        confirm = driver.switch_to.alert
        confirm.accept()

    @classmethod
    def quxiao(cls, driver, cmd):
        # 处理取消弹窗
        confirm = driver.switch_to.alert
        confirm.dismiss()
