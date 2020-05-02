from selenium import webdriver as wd
from bs4 import BeautifulSoup
import time
import argparse

def getText(html_tag):
    return html_tag.replace('\n', '').replace('\t', '').replace(' ','')

def getJson(tag):
    json = {}
    user_channel = tag.select('a.ytd-comment-renderer')[0].get('href')
    json['user_channel'] = user_channel

    user_text = tag.select('a.ytd-comment-renderer > span')[0].text
    json['user_text'] = getText(user_text)

    user_image = tag.select('img.yt-img-shadow')[0].get('src')
    json['user_image'] =user_image

    user_time = tag.select('a.yt-formatted-string')[0].text
    json['user_time'] = getText(user_time);

    user_comment_good_count = tag.select('span.ytd-comment-action-buttons-renderer')[0].text
    json['user_comment_good_count'] = getText(user_comment_good_count)

    user_comment = tag.select('div.ytd-expander')[0]
    json['user_comment'] = user_comment

    # user_expander_comment = tag.select('div.ytd-comment-replies-renderer')
    # if not user_expander_comment:
    #     json['user_expander_comment'] = getText(user_expander_comment[0].text);
    print(json)
    return json;

parser = argparse.ArgumentParser(description='유튜브 댓글을 크롤링합니다.')
parser.add_argument('--url', required=True, help='유튜브 주소를 입력해주세요')

args = parser.parse_args()

driver = wd.Chrome(executable_path="/usr/local/bin/chromedriver")
url = args.url
driver.get(url)

last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(3.0)
    new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    if new_page_height == last_page_height:
        break
    last_page_height = new_page_height

html_source = driver.page_source

driver.close()

soup = BeautifulSoup(html_source, 'lxml')

result_list = []

youtube_tags = soup.select('div.ytd-item-section-renderer ytd-comment-thread-renderer.ytd-item-section-renderer')

for tag in youtube_tags:
    print(tag)
    result_list.append(getJson(tag))
    print("===========")
    print(getJson(tag))
    print("")
    print("")

print(result_list)
