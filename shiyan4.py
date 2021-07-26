#利用excel将专业分数线表筛选成高校分数线表，然后将表读取到数据库中
# coding=utf-8
import mysql.connector
import xlrd

my_db = mysql.connector.connect(
    host="localhost",  # 如果服务器是本机用loacalhost，如果服务器是远程，用IP地址。
    user="root",  # 用户名
    passwd="123456",  # 密码
    auth_plugin="mysql_native_password"
)
mycursor = my_db.cursor()
mycursor.execute("use test1")#连接数据库
sql = "create table aa学校分数线 (id int(100) primary key AUTO_INCREMENT ,学校 varchar(100) ,分数线 int(100))"
mycursor.execute(sql)

s = xlrd.open_workbook("C:/Users/123/Desktop/分数线1.xlsx")
sheet_name = s.sheets()[0]

x=0
while x!=1009:
    x+=1
    school_name = sheet_name.cell(x, 1).value
    school_name = school_name[4:]
    mark=sheet_name.cell(x,5).value
    sql="insert into aa学校分数线 (学校,分数线) values('{}','{}')".format(school_name,mark)
    mycursor.execute(sql)
    my_db.commit()
