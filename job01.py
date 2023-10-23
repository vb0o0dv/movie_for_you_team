from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchCookieException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime


options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")


service = ChromeService(executable_path=ChromeDriverManager().install())
# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경



year = 2019
month = 9
set_title = set()
for i in range(1):
    ranking_url = 'https://movie.daum.net/ranking/boxoffice/monthly?date={}{:02d}'.format(year,month)
    driver.get(ranking_url)
    datas = []
    time.sleep(1)
    for j in range(1,31):
        try:
            title_tag = driver.find_element('xpath','//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(j))
            title = title_tag.text
        except:
            print('error 영화 제목 못가져옴 {}년 {}월 {}번째 영화'.format(year,month,j))
            continue
        if title in set_title:
            continue
        else:
            set_title.add(title)
        title_tag.click()
        time.sleep(1)
        try:
            review_tag = driver.find_element('xpath','//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span')
            review_tag.click()
            time.sleep(2)
        except:
            print('{} 평점 못 눌룸 {}'.format(title,j))
            ranking_url = 'https://movie.daum.net/ranking/boxoffice/monthly?date={}{:02d}'.format(year, month)
            driver.get(ranking_url)
            continue
        for k in range(5):
            try:
                more_button = driver.find_element('xpath', '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button')
                if more_button:
                    more_button.click()
                    time.sleep(1)
                else:
                    print('error {} 더보기 누른 회수{}'.format(title, k))
                    break
            except:
                print('error 더보기 버튼 {} {}'.format(title,k))
                break
        review_count = driver.find_element('xpath','//*[@id="mainContent"]/div/div[2]/div[2]/div/strong/span').text
        review_count  = int(re.compile('[^0-9]').sub('',review_count))
        for k in range(1,min(review_count+1,161)):
            try:
                reviews = driver.find_element('xpath','/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(k))
                if reviews:
                    review = reviews.text
                    review = re.compile('[^가-힣]').sub(' ',review)
                    datas.append([title,review])
                else:
                    print('{} {} 여기서 리뷰 끝'.format(title, k))
                    break
            except:
                print('error 리뷰 문제 {} {}'.format(title, k))
        ranking_url = 'https://movie.daum.net/ranking/boxoffice/monthly?date={}{:02d}'.format(year, month)
        driver.get(ranking_url)
    df_data = pd.DataFrame(datas,columns=['title','review'])
    df_data.to_csv('./crawling_data/review_{}{:02d}.csv'.format(year,month),index=False)
    month-=1
    if month<=0:
        year-=1
        month=12

driver.close()


