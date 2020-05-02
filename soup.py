from bs4 import BeautifulSoup

json = {}

def getText(html_tag):
    return html_tag.replace('\n', '').replace('\t', '').replace(' ','')

with open("test.html", "r") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    # print(soup)

    user_channel = soup.select('a.ytd-comment-renderer')[0].get('href')
    json['user_channel'] = user_channel

    user_text = soup.select('a.ytd-comment-renderer > span')[0].text
    json['user_text'] = getText(user_text)

    user_image = soup.select('img.yt-img-shadow')[0].get('src')
    json['user_image'] =user_image

    user_time = soup.select('a.yt-formatted-string')[0].text
    json['user_time'] = getText(user_time);

    user_comment_good_count = soup.select('span.ytd-comment-action-buttons-renderer')[0].text
    json['user_comment_good_count'] = getText(user_comment_good_count)

    user_comment = soup.select('div.ytd-expander')[0]
    json['user_comment'] = user_comment

    user_expander_comment = soup.select('div.ytd-comment-replies-renderer')
    if not user_expander_comment:
        json['user_expander_comment'] = getText(user_expander_comment);

    print(json)
