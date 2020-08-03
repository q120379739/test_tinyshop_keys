#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/10/21 17:37
#存放公共模块脚本
import datetime
import time,json
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pymysql
from configparser import ConfigParser


class common_utility():
    def __init__(self):
        self.sql_addr = common_utility.get_config('clint_db','sql_addr')
        self.sql_user = common_utility.get_config('clint_db','sql_user')
        self.sql_psword = common_utility.get_config('clint_db','sql_psword')
        self.sql_database = common_utility.get_config('clint_db','sql_database')
        global sql_addr
        global sql_user
        global sql_psword
        global sql_database
        sql_addr = self.sql_addr
        sql_user = self.sql_user
        sql_psword = self.sql_psword
        sql_database = self.sql_database

    # @classmethod
    # def is_element_present(self,how,what):
    #     #判断元素存不存在
    #     try:
    #         common_utility.dr.find_element(by=how,value=what)
    #         return True
    #     except NoSuchElementException as e:
    #         return False
    #     return True

    @classmethod
    def write_html(cls,version,moban_file_addr,fileaddr):
        #连接数据库查询并写入本地html文件
        conn = pymysql.connect(host=sql_addr, user=sql_user, passwd=sql_psword, database=sql_database, charset='utf8')
        cursor = conn.cursor()
        sql = "select * from testdb where version='%s'" % version
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        if result == ():
            print("此次测试过程,没有测试结果产生")
            return

        moban_file = open(moban_file_addr, 'r', encoding='utf-8')
        content = moban_file.read()
        # 获取版本信息并替换模板变量
        version = result[0][1]
        # 通用版本查询SQL语句
        sql_base = "select count(*) from testdb where version="
        # 获取成功数量并替换模板变量
        sql_pass = sql_base + "'%s' and result='成功'" % version
        cursor.execute(sql_pass)
        pass_count = cursor.fetchone()[0]
        # 获取失败数量并替换模板变量
        sql_fail = sql_base + "'%s' and result='失败'" % version
        cursor.execute(sql_fail)
        fail_count = cursor.fetchone()[0]
        # 获取错误数量并替换模板变量
        sql_error = sql_base + "'%s' and result='错误'" % version
        cursor.execute(sql_error)
        error_count = cursor.fetchone()[0]
        # 获取特定version的最后一个用例时间
        sql_last = "select testtime from testdb where version='%s' order by id desc limit 0,1" % version
        cursor.execute(sql_last)
        lasttime = cursor.fetchone()[0]
        lasttime = str(lasttime)
        ele2 = []
        mydict = {"testPass": pass_count, "testResult": ele2, "testName": "TinyShop",
                  "testAll": pass_count + fail_count,
                  "testFail": fail_count,
                  "beginTime": lasttime,
                  "totalTime": lasttime,
                  "testSkip": 0}
        for i in result:
            if i[9] != '无':
                abcc = '<img src="' + i[9] + '" alt="无错误截图" />'
                ele1 = {"className": str(i[2]), "methodName": i[3], "description": i[5], "spendTime": i[4],
                        "status": i[6], "log": [str(i[7])+'\n',i[8], abcc]}
                ele2.append(ele1)
            else:
                ele1 = {"className": str(i[2]), "methodName": i[3], "description": i[5], "spendTime": i[4],
                        "status": i[6],
                        "log": [str(i[7])+'\n',i[8], i[9]]}
                ele2.append(ele1)
        mydict = json.dumps(mydict)
        ele3 = content.replace("${resultData}", mydict)
        report_file = open(fileaddr, 'w',
                           encoding='utf-8')
        report_file.write(ele3)
        print("生成HTML报告成功")

    @classmethod
    def insert_data(cls,version,module,testtype,caseid,casetitle,result,error,screenshot):
        #对数据库插入数据
        testtime= time.strftime("%Y-%m-%d %X")
        conn = pymysql.connect(host='localhost',user='root',passwd='123456',database='woniuatmtest',charset='utf8')
        cursor = conn.cursor()
        casetitle = casetitle.replace("'","")
        error = str(error).replace("'","")
        sql = "insert into testdb(version,module,testtype,caseid,casetitle,result,testtime,error,screenshot) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(version,module,testtype,caseid,casetitle,result,testtime,error,screenshot)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def get_erroe_img(cls,dr,fileaddrs="C:/Users/bbb/PycharmProjects/test_tinyshop_keys/img/"):
        #截图
        filename = time.strftime("%Y%m%d%H%M%S") + ".png"
        files = fileaddrs+filename
        dr.get_screenshot_as_file(files)
        return files

    @classmethod
    def result(cls,case,file_addr):
        #记录日志
        nowtime = time.strftime("%Y-%m-%d.%X")
        with open(file_addr,'a+',encoding="GBK") as f:
            f.write(nowtime+','+case+'\n')

    @classmethod
    def get_csvs(cls, filds):
        with open(filds, encoding='gbk') as opp:
            cmds = []
            cmdd = []
            ele = opp.read().split("skip")
            for i in range(0, len(ele)):
                if not ele[i].startswith('#'):
                    cmds.append(ele[i])
            for j in cmds:
                ele2 = j.split('\n')
                cmdd.append(ele2)
        return cmdd

    @classmethod
    def get_config(cls, section, key):
        # 读取配置文件
        config = ConfigParser()
        config.read(r'C:\Users\bbb\PycharmProjects\test_tinyshop_keys\data\config.conf', encoding='utf-8')
        return config.get(section, key)
