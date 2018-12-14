from selenium import webdriver
import time
import re
import json

g_qzonetoken = ''
gtk = ''

print('初始化爬虫功能...')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='../resource/chromedriver/chromedriver')


def get_login_info(qq_num, qq_pass):

    global g_qzonetoken
    global gtk

    driver.get('https://qzone.qq.com/')
    print("获取登录页面：https://qzone.qq.com/")

    driver.switch_to.frame('login_frame')
    driver.find_element_by_id('switcher_plogin').click()
    time.sleep(0.5)

    driver.find_element_by_id('u').clear()
    driver.find_element_by_id('u').send_keys(qq_num)  # 这里填写你的QQ号
    driver.find_element_by_id('p').clear()
    driver.find_element_by_id('p').send_keys(qq_pass)  # 这里填写你的QQ密码

    driver.find_element_by_id('login_button').click()
    print("登录")
    time.sleep(3)

    # ---------------获得g_qzonetoken 和 gtk
    html = driver.page_source
    g_qzonetoken = re.search('window\.g_qzonetoken = \(function\(\)\{ try\{return (.*?);\} catch\(e\)',html)#从网页源码中提取g_qzonetoken
    g_qzonetoken = str(g_qzonetoken[0]).split('\"')[1]
    cookie = {}  # 初始化cookie字典
    for elem in driver.get_cookies():  # 取cookies
        cookie[elem['name']] = elem['value']

    gtk = get_gtk(cookie)  # 通过getGTK函数计算gtk
    print('获取 g_qzonetoken ：' + g_qzonetoken)
    print('获取 gtk ：' + str(gtk))


def get_gtk(cookie):
    hashes = 5381
    for letter in cookie['p_skey']:
        hashes += (hashes << 5) + ord(letter)
    return hashes & 0x7fffffff


def crawler_emotion(uin, skip, num):  # 爬取说说数据 uin：好友qq、skip：跳过前 skip 条、num：一次获取说说条数（测试最大应该为40条）

    msg_dict = ""

    driver.get(
        'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=' + uin + '&ftype=0&sort=0&pos=' + str(
            skip) + '&num=' + str(num) + '&replynum=200&g_tk=' + str(
            gtk) + '&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1&qzonetoken=' + str(
            g_qzonetoken) + '&g_tk=' + str(gtk))
    try:
        msg_list_json = driver.page_source
        msg_list_json = str(msg_list_json)
        # 检测是否没有权限访问
        abtract_pattern = re.compile(',"message":"(.*?)","name":', re.S)
        message = re.findall(abtract_pattern, str(msg_list_json))
        if message != []:
            if str(message[0]) == '对不起,主人设置了保密,您没有权限查看':  # 对不起,主人设置了保密,您没有权限查看
                print('对不起,主人设置了保密,您没有权限查看')

        msg_list_json = msg_list_json.split("_preloadCallback(")[1]  # 拆分json，缩小范围，也能加快解析速度
        msg_list_json = msg_list_json.split(");</pre></body></html>")[0]

        msg_dict = json.loads(msg_list_json)
    finally:
        return msg_dict['msglist']


# get_login_info('1926791261', 'hanghang183367.')
# print(crawler_emotion('449338017', 0, 10))
