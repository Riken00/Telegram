import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

path = 'message.csv'

def login(driver, username, password):
    login_url = 'https://twitter.com/i/flow/login'
    driver.get(login_url)
    time.sleep(2)

    # username/email field
    username_field = driver.find_element_by_xpath('//input[@autocomplete="username"]')
    if not username_field: return False
    username_field.send_keys(username)
    time.sleep(2)

    # click on next button
    driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[6]').click()
    # driver.find_element_by_class_name('css-18t94o4.css-1dbjc4n.r-42olwf.r-sdzlij.r-1phboty.r-rs99b7.r-ywje51.r-usiww2.r-2yi16.r-1qi8awa.r-1ny4l3l.r-ymttw5.r-o7ynqc.r-6416eg.r-lrvibr.r-13qz1uu').click()
    time.sleep(1)

    # password field
    password_field = driver.find_element_by_xpath('//input[@autocomplete="current-password"]')
    password_field.send_keys(password)
    time.sleep(2)

    # click on login btn
    driver.find_element_by_class_name('css-18t94o4.css-1dbjc4n.r-sdzlij.r-1phboty.r-rs99b7.r-ywje51.r-usiww2.r-peo1c.r-1ps3wis.r-1ny4l3l.r-1guathk.r-o7ynqc.r-6416eg.r-lrvibr.r-13qz1uu').click()
    time.sleep(2)


def get_quote_tweets(driver, account_name, tweet_id):
    url = f'https://twitter.com/{account_name}/status/{tweet_id}/retweets/with_comments'
    # print('3')
    driver.get(url)
    time.sleep(4)
    # print('2')
    
    total_sub_tweet = driver.find_elements_by_xpath('//div[@class="css-1dbjc4n r-j5o65s r-qklmqi r-1adg3ll r-1ny4l3l"]')
    # print(total_sub_tweet,'-----------------------5876515414534874534986456186')
    # print('11111111')
    time.sleep(2)
    data = [['message','link']]
    for i in total_sub_tweet:   
        sub_twit_div = i.find_element_by_xpath('.//div[@class="css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"]')
        sub_text = sub_twit_div.find_element_by_xpath('.//span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]')
        twit_text_link = i.find_element_by_xpath('.//a[@class="css-4rbku5 css-18t94o4 css-901oao r-14j79pv r-1loqt21 r-1q142lx r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0"]')
        print("-----************************dasdsadsad********",sub_text.text)
        print("-----************************dasdsadsad********",twit_text_link.get_attribute('href'))
        tw_message = sub_text.text
        tw_link = twit_text_link.get_attribute('href')
        lists = [tw_message,tw_link]
        data.append(lists)
    data = pd.DataFrame(data)
    data.to_csv(path,index=False)
    # for i in total_sub_tweet:
    #     abc = i.find_element_by_xpath('.//div[@class="css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"]')
    #     texsss = abc.find_element_by_xpath('.//span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]')
    #     link = i.find_element_by_xpath('.//a[@class="css-4rbku5 css-18t94o4 css-901oao r-14j79pv r-1loqt21 r-1q142lx r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0"]')
    #     print("-----************************dasdsadsad********",texsss.text)
    #     print("-----************************dasdsadsad********",link.get_attribute('href'))

    #     # texsss.click()
    #     # time.sleep(2)
    #     # print(driver.current_url)

    #     # driver.back()
    #     # time.sleep(3)
    #     # texsss = i.find_element_by_class_name('css-16my406')
        
    #     # print("-----********************************",texsss)
    #     # print(i,'-'*50)
    print('11111111')
    import pdb;pdb.set_trace()



if __name__ == '__main__':
    username = 'EmpiricRiken'
    password = 'Rk.empiric'

    driver = webdriver.Chrome('./chromedriver')
    
    driver.maximize_window()

    # perform login if not already
    login(driver, username, password)

    get_quote_tweets(driver, 'ultraman_nft', 1483319527186251779)
