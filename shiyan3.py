# coding=utf-8
import mysql.connector
import xlrd
import re

my_db = mysql.connector.connect(
    host="localhost",  # 如果服务器是本机用loacalhost，如果服务器是远程，用IP地址。
    user="root",  # 用户名
    passwd="123456",  # 密码
    auth_plugin="mysql_native_password"
)
mycursor = my_db.cursor()
mycursor.execute("use test1")#连接数据库


s = xlrd.open_workbook("C:/Users/123/Desktop/分数线.xlsx")
#原因：xlrd更新到了2.0.1版本，只支持.xls文件，不支持.xlsx。
#解决办法：安装旧版本1.2.0
sheet_name = s.sheets()[0]#获取表名。打印出来可能不对，没关系，不碍事
#excel表格从1开始，而坐标从0开始
with open("C:/Users/123/Desktop/test_1.txt","w",encoding='utf-8') as f:
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        f.write("{}".format(x))#将所有表名存入文本文件，然后再正则提取，或许可以直接正则，可以一试
with open('C:/Users/123/Desktop/test_1.txt','r',encoding='utf-8')as f:
    source=f.read()
s_list=re.findall('\(\'(.*?)\'',source,re.S)


x=2
while x!=16716:
    x+=1
    school_name=sheet_name.cell(x,1).value
    school_name=school_name[4:]
    subject_name=sheet_name.cell(x,0).value
    subject_name=subject_name[2:]
    mark=sheet_name.cell(x,5).value
    if (school_name not in s_list):
        continue
    #判断表名是否存在，比如北京建筑大学就不在已创建的表里
    mycursor.execute("update `{}` set 专业分数线={} where 专业名称='{}'".format(school_name,mark, subject_name))
    my_db.commit()












