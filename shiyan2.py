#从山东省教育招生考试院爬取高考选考科目要求
# coding=utf-8
import requests
import re
import mysql.connector


requests.packages.urllib3.disable_warnings()
html = requests.get('https://xkkm.sdzk.cn/web/xx.html', verify=False)
html_1 = html.content.decode()
content_list = re.findall('name="mc" value=\'(.*?)\'', html_1, re.S)
shibai_list = re.findall('name="dm" value=\'(.*?)\'', html_1, re.S)

my_db = mysql.connector.connect(
    host="localhost",  # 如果服务器是本机用loacalhost，如果服务器是远程，用IP地址。
    user="root",  # 用户名
    passwd="123456",  # 密码
    auth_plugin="mysql_native_password"
)
mycursor = my_db.cursor()
mycursor.execute("use test2")

def find_1(post_dm, post_mc):
    data_1 = {
        'dm': post_dm,
        'mc': post_mc,
        'yzm': 'ok'

    }
    html = requests.post('https://xkkm.sdzk.cn/xkkm/queryXxInfor', data=data_1,verify=False).content.decode()
    return html


def school_name(post_dm0, post_mc0):
    html_1 = find_1(post_dm0, post_mc0)
    name_search = re.search('学校名称：</span><span style="color: #0044CC; font-weight: bold; font-size: 18px;">(.*?)<',
                            html_1, re.S).group(1)
    return name_search  # 获取学校名字


def create_table(mingzi):
    sql = "create table `" + mingzi + "` (id int(100) primary key AUTO_INCREMENT ,subjectname varchar(100) ,subjectrequest varchar(100),first varchar(100),second varchar(100),subjectmark int(100))"
    print(sql)
    mycursor.execute(sql)
    # 创建学校名对应的表


def insert_table(post_dm_1, post_mc_1):
    print("post_dm_1----->", post_dm_1)
    print("post_mc_1----->", post_mc_1)
    html_2 = find_1(post_dm_1, post_mc_1)
    name_school = school_name(post_dm_1, post_mc_1)
    name_subject_list = re.findall('"25%" align="left"style="display:table-cell; vertical-align:middle;">(.*?)<',
                                   html_2, re.S)
    name_subject_list = [item.replace('\r\n', '') for item in name_subject_list]
    name_subject_list = [item.replace(' ', '') for item in name_subject_list]
    for x in name_subject_list:
        mycursor.execute("insert into `{}` (subjectname) values('{}')".format(name_school,x))
        my_db.commit()


def Is_char(char_1):
    if char_1 == '不提科目要求':
        return 1
    else:
        if '方可' in char_1:
            if '1门' in char_1:
                return 2  # 一门科目考生必须选考方可报考
            else:
                return 3  # 两门科目考生均须选考方可报考
        else:
            return 4  # 两门科目考生选考其中一门即可报考


def demand(post_dm1, post_mc1):
    html_3 = find_1(post_dm1, post_mc1)
    demand_list = re.findall('"30%" align="left" style="display:table-cell; vertical-align:middle;">(.*?)<', html_3,
                             re.S)
    name_school = school_name(post_dm1, post_mc1)
    id1 = 0
    for s in demand_list:
        id1 += 1
        a = Is_char(s)
        if a == 1:
            mycursor.execute("update `{}` set subjectrequest='不提科目要求' where id={}".format(name_school,id1))
            my_db.commit()
        elif a == 2:
            mycursor.execute("update `{}` set subjectrequest='一门科目考生必须选考方可报考' where id={}".format(name_school,id1))
            mycursor.execute("update `{}` set first='{}' where id={}".format(name_school,s[0:2],id1))
            my_db.commit()
        elif a == 3:
            mycursor.execute("update `{}` set subjectrequest='两门科目考生均须选考方可报考' where id={}".format(name_school,id1))
            mycursor.execute("update `{}` set first='{}' where id={}".format(name_school,s[0:2],id1))
            mycursor.execute("update `{}` set second='{}' where id={}".format(name_school,s[3:5],id1))
            my_db.commit()
        else:
            mycursor.execute("update `{}` set subjectrequest='两门科目考生选考其中一门即可报考' where id={}".format(name_school,id1))
            mycursor.execute("update `{}` set first='{}' where id={}".format(name_school,s[0:2],id1))
            mycursor.execute("update `{}` set second='{}' where id={}".format(name_school,s[3:5],id1))
            my_db.commit()


for (post_mc4, post_dm4) in zip(content_list, shibai_list):
    name_1 = school_name(post_dm4, post_mc4)
    create_table(name_1)
    insert_table(post_dm4, post_mc4)
    demand(post_dm4, post_mc4)


