# coding=utf8
import itchat
import time
import datetime
import threading
import UserDB
import JokeDB

# http://www.liuxue86.com/a/3151933.html


# 系统客户微信账号
admin = ['shen']

getup_hour = 7 # 起床时间
getup_min = 0 # 起床时间

sign_hour = 8 #上班时间
sign_min = 20 #上班时间

lunch_hour = 11 #午饭时间
lunch_min = 30 #午饭分钟

offwork_hour = 17 #下班小时
offwork_min = 30 #下班分钟

sign_out_hour = 17 #签退时间
sign_out_min =  36 #签退时间

extra_hour = 20 #加班时间
extra_min = 0 #加班

sleep_hour = 23 #睡觉时间
sleep_min = 0 #睡觉时间

joke_hour = 12 #睡觉时间
joke_min = 0 #睡觉时间


def not_empty(s):
    return s and s.strip()


# 自动回复
# 封装好的装饰器，当接收到的消息是Text，即文字消息
@itchat.msg_register('Text')
def text_reply(msg):
    # 当消息不是由自己发出的时候
    if not msg['FromUserName'] == myUserName:
        # 发送一条提示给文件助手
        itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
                        (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                         msg['User']['NickName'],
                         msg['Text']), 'filehelper')
        send_msg_to_admin(msg=msg['Text'])
        # 回复给好友
        return u'[自动回复]您好，我只是段代码，有事请联系我的主人---Jerry。\n 您的的信息：%s  我会转达给 Jerry \n' % (msg['Text'])


# 起床
def notify_getup():
    print("一天之际在于晨，起床啦")
    send_msg_to_admin('一天之际在于晨，起床啦')
    notify_myself('骚年，上班啦，记得签到啊！')


# 签到
def notify_sign():
    print("骚年，上班啦，记得签到啊！")
    send_msg_to_admin("【微信提醒】骚年，上班啦，记得签到,打卡啊！")
    notify_myself('骚年，上班啦，记得签到啊！')


# 午饭
def notify_lunch():
    print("人是铁饭是钢，午饭，走起！")
    send_msg_to_admin("人是铁饭是钢，午饭，走起！")
    notify_myself('人是铁饭是钢，午饭，走起！')


# 一起下班
def notify_off_work():
    print("一天最美的事，莫过于下班，下班，走起！")
    send_msg_to_admin("【微信提醒】一天最美的事，莫过于下班，打卡，签退，走起！")
    notify_myself('一天最美的事，莫过于下班，打卡，签退，走起！')


# 签退
def notify_sign_out():
    print("枯藤老树昏鸦，上班下班回家")
    send_msg_to_admin("【微信提醒】一天最美的事，莫过于下班，但不要忘了签退")
    notify_myself('一天最美的事，莫过于下班，打卡，签退，走起！')


# 加班
def notify_extra_work():
    print("加班写代码中")
    send_msg_to_admin("【微信提醒】加吧正常，经常加班就不好了，打卡，签退，回吧！")
    notify_myself('一天最美的事，莫过于下班，打卡，签退，走起！')


# 睡觉
def notify_sleep():
    print("垂死病中惊坐起，今日到底星期几。抬望眼，卧槽，周一。低头，完了，十点。")


# 根据通讯录中名字，向微信好友集合发送消息
def notify_we_chat(msg, person):
    print(msg, person)
    for p in person:
        if p == "":
            print("名字为空不进行发送")
        else:
            # 想给谁发信息，先查找到这个朋友
            users = itchat.search_friends(name=p)
            # 找到UserName
            userName = users[0]['UserName']
            # 然后给他发消息
            itchat.send(msg, toUserName=userName)


# 向自己文件传输助手发消息
def notify_myself(msg):
    itchat.send(msg, 'filehelper')


# 向指定的开发人员发送系统提示消息
def notify_admin():
    notify_we_chat("【提醒小能手】系统运行正常，请主人放心", admin)


# 向指定的开发人员发送 msg 消息
def send_msg_to_admin(msg):
    notify_we_chat(msg, admin)


# 实时监控线程
class we_chat_thread (threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        notify_admin()
        while True:

            localtime = time.localtime(time.time())
            # 格式化成2016-03-20 11:45:39形式
            print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

            day_of_week = datetime.datetime.now().weekday()
            print("今天是星期", day_of_week + 1)

            s_hour = localtime.tm_hour
            s_min = localtime.tm_min

            print("现在时间：", s_hour, ":", s_min)

            #s_hour = int(input("请输入小时："))
            #s_min = int(input("请输入分钟："))

            # 每半小时通知一次
            if s_min == 30 or s_min == 0:
                notify_admin()

            if day_of_week == 5 or day_of_week == 6:
                print("今天是周末")
                time.sleep(60 * 20)
            # 进行提示
            elif getup_hour == s_hour and getup_min == s_min:
                notify_getup()
            elif sign_hour == s_hour and sign_min == s_min:
                notify_sign()
            elif lunch_hour == s_hour and lunch_min == s_min:
                notify_lunch()
            elif offwork_hour == s_hour and offwork_min == s_min:
                notify_off_work()
            elif sign_out_hour == s_hour and sign_out_min == s_min:
                notify_sign_out()
            elif extra_hour == s_hour and extra_min == s_min:
                notify_extra_work()
            elif sleep_hour == s_hour and sleep_min == s_min:
                notify_sleep()
            elif joke_hour == s_hour and joke_min == s_min:
                send_joke_msg()
            if s_hour < (getup_hour - 1) or s_hour > (sleep_hour + 1):
                time.sleep(60 * 20)
            else:
                time.sleep(60)


# 向微信发送消息
def notify_we_chat_by_user(msg, user):

    print("开始-----向", user['name'], "发送消息: ", msg)

    if user == "":
            print("名字为空不进行发送")
    else:
        content = user['hint'] + '：\n' + msg
        # 想给谁发信息，先查找到这个朋友
        users = itchat.search_friends(name=user['nick'])
        # 找到UserName
        user_name = users[0]['UserName']
        # 然后给他发消息
        itchat.send(content, toUserName=user_name)

    print("结束-----向", user['name'], "发送消息: ", msg)


# 向微信所有好友发送消息
def notify_all_we_chat(message):
    print("开始-----向所有好友发送消息")

    friend_list = itchat.get_friends(update=True)

    for friend in friend_list:

        itchat.send('hello', toUserName=friend['UserName'])

        print("向微信好友", friend['NickName'], friend['Signature'], '发送消息：', message)

    print("结束-----向所有好友发送消息")


# 向通讯录中的所有用户发送joke
def send_joke_msg_to_all():
    print("开始-----joke------向所有好友发送消息")
    user_db = UserDB.query_user_data()

    joke_data = JokeDB.query_joke_data_desc()

    jokes = joke_data['data']

    joke = jokes[0]

    joke_content = joke['content']

    joke_id = joke['id']

    JokeDB.update_chat_state(joke_id)

    users = user_db['data']

    for user in users:
        notify_we_chat_by_user(joke_content, user)
        JokeDB.update_chat_state(joke_id)
    print("结束-----joke------向所有好友发送消息")


# 向数据库中的用户发送joke
def send_joke_msg():
    print("开始-----joke------向数据库发送消息")

    user_db = UserDB.query_user_data()

    joke_data = JokeDB.query_joke_data_desc()

    jokes = joke_data['data']

    joke = jokes[0]

    joke_content = joke['content']

    joke_id = joke['id']

    JokeDB.update_chat_state(joke_id)

    users = user_db['data']

    for user in users:
        notify_we_chat_by_user(joke_content, user)
        JokeDB.update_chat_state(joke_id)

    print("开始-----joke------向数据库发送消息")


if __name__ == '__main__':


    ''''
    itchat.auto_login()

    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    # 向自己文件传输助手发消息
    itchat.send(u"开始", 'filehelper')


    # 想给谁发信息，先查找到这个朋友
    users = itchat.search_friends(name=u'吴佳健')
    # 找到UserName
    userName = users[0]['UserName']
    # 然后给他发消息
    itchat.send('hello', toUserName=userName)

    #user = itchat.search_friends(name=u'吴佳健')[0]
    #user.send(u'机器人say hello')

    # 想给谁发信息，先查找到这个朋友
    users = itchat.search_friends()
    # 找到UserName
    userName = users[0]['UserName']
    # 然后给他发消息
    itchat.send('hello', toUserName=userName)

    itchat.run()'''

    # itchat.auto_login()
    #
    # # 获取自己的UserName
    # myUserName = itchat.get_friends(update=True)[0]["UserName"]

    itchat.auto_login()

    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    # 向自己文件传输助手发消息
    itchat.send(u"系统开始运行", 'filehelper')
    print("系统开始运行")

    # 创建线程
    try:
        we_chat = we_chat_thread(1, "we_chat_thread")
        we_chat.start()
    except:
        print("Error: 无法启动线程")

    itchat.run()

    #tchat.send(u"系统退出运行", 'filehelper')


