from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from lxml import html
import time
import csv

# 因为使用cookies，不能读取页面内容，采用登录方式
def twitter_login():
    url = 'https://twitter.com/login'
    driver.get(url)
    input_username = driver.find_element_by_name("session[username_or_email]")
    input_username.send_keys(" ") #你的userid/注册email等
    input_password = driver.find_element_by_name("session[password]")
    input_password.send_keys(" ") #你的密码
    button = driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[3]/div/div/span')
    button.click()
    time.sleep(1)

#为了避免过多的非正规操作，进行登出操作
def twitter_logout():
    url = 'https://twitter.com/logout'
    driver.get(url)
    time.sleep(3)
    button = driver.find_element(By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div[3]/div[2]/div/span')
    button.click()
    time.sleep(1)

# 推文，点赞数爬取
def tweets_get():

    userid = 'dongfangleiatu' #要爬取的用户的userid
    url = 'https://twitter.com/{}'.format(userid)
    driver.get(url)
    time.sleep(5)
    time_set = set()
    filename = '{}.csv'.format(userid)
    stop = None
    with open(filename, "a", newline='',encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['twitter_content','twitter_like'])
        while True:

            ht = html.fromstring(driver.page_source)
            tweets = ht.xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div/div')
            first_time = ht.xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div/div[1]/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/a/time/@datetime')
            if first_time == stop:
                break
            else:
                stop = first_time

            for tweet in tweets:
                tweet_time = tweet.xpath('div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/a/time/@datetime')
                if tweet_time:
                    if tweet_time[0] in time_set:
                        continue
                    time_set.add(tweet_time[0])
                    twitter_content = tweet.xpath('div/div/article/div/div/div/div[2]/div[2]/div[2]/div[@class="css-1dbjc4n"]/div/span[@class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"]/text()')
                    if not twitter_content:
                        twitter_content = ['ONLY img(只有图片或者表情)']
                    twitter_like = tweet.xpath('div/div/article/div/div/div/div[2]/div[2]/div[2]/div[@aria-label]/div[3]/div/div/div[2]/span/span[@class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"]/text()')
                    if not twitter_like:
                        twitter_like = [0]
                    tweet_list = [twitter_content[0],twitter_like[0]] #解决0赞时为空的问题
                    writer.writerow(tweet_list)


            for i in range(5):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
                #driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(0.5)

#following列表爬取
def twitter_following():

    userid = 'Kana_Momonogi'
    url = 'https://twitter.com/{}/following'.format(userid)
    driver.get(url)
    time.sleep(5)
    stop = None
    uid_set = set()
    filename = '{}_following.csv'.format(userid)
    #python 默认打开gbk，写入csv的utf-8用excel打开会中文乱码，改为utf-8-sig
    with open(filename,'a',newline='',encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file,delimiter=',')
        writer.writerow(['username','userid'])
        while True:
            time.sleep(0.4)
            ht = html.fromstring(driver.page_source)
            users = ht.xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/section/div/div/div')
            first_userid = ht.xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/section/div/div/div[1]/div/div/div/div[2]/div[1]/div[1]/a/div/div[2]/div/span/text()')
            if stop == first_userid:
                break
            else:
                stop = first_userid

            for user in users:
                raw_userid = user.xpath('div/div/div/div[2]/div[1]/div[1]/a/div/div[2]/div/span/text()')

                if raw_userid:
                    if raw_userid[0] in uid_set:
                        continue
                    uid_set.add(raw_userid[0])
                    userid = raw_userid[0][1:]
                    username = user.xpath('div/div/div/div[2]/div[1]/div[1]/a/div/div[1]/div[1]/span/span/text()')
                    user_list = [username[0],userid]
                    writer.writerow(user_list)

            for i in range(3):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
                #driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(0.3)
    time.sleep(5)

#followers列表爬取
def twitter_followers():

    userid = 'HanakovaEva'
    url = 'https://twitter.com/{}/followers'.format(userid)
    driver.get(url)
    time.sleep(5)
    stop = None
    uid_set = set()
    filename = '{}_followers.csv'.format(userid)
    with open(filename,'a',newline='',encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file,delimiter=',')
        writer.writerow(['username','userid'])
        while True:

            time.sleep(0.4)
            ht = html.fromstring(driver.page_source)
            users = ht.xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/section/div/div/div')
            first_userid = ht.xpath(
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/section/div/div/div[1]/div/div/div/div[2]/div[1]/div[1]/a/div/div[2]/div/span/text()')
            if stop == first_userid:
                break
            else:
                stop = first_userid

            for user in users:
                raw_userid = user.xpath('div/div/div/div[2]/div[1]/div[1]/a/div/div[2]/div/span/text()')

                if raw_userid:
                    if raw_userid[0] in uid_set:
                        continue
                    uid_set.add(raw_userid[0])
                    userid = raw_userid[0][1:]
                    username = user.xpath('div/div/div/div[2]/div[1]/div[1]/a/div/div[1]/div[1]/span/span/text()')
                    user_list = [username[0],userid]
                    writer.writerow(user_list)

            for i in range(3):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
                #driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(0.3)
    time.sleep(5)

if __name__ == '__main__':

    try:
        #webdriver的路径
        driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
        #显式等待，结合EC(expected_conditions)使用
        #wait = WebDriverWait(driver, 10)

        twitter_login()

        #tweets_get()

        twitter_following()

        #twitter_followers()

        twitter_logout()

    finally:

        driver.quit()
'''
ht = html.fromstring(driver.page_source)
twitter_content = ht.xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span[1]/text()')
twitter_like = ht.xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div[3]/div/div/div[2]/span/span/text()')
#print(driver.page_source)
print(twitter_content)
print(twitter_like)
print(len(twitter_content))
print(len(twitter_like))
twitter_pair = list(zip(twitter_content,twitter_like))
print(twitter_pair)
'''


