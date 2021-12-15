import requests
import json
from bs4 import BeautifulSoup
import urllib
import time
import os

base_url = "https://dlsoft.dmm.co.jp/subsc/li/?page="

dmm_cookie = {"age_check_done": "1"}

def conv_dic(soup):
    """
    ネストされた辞書を返す

    htmlの中にタグが無い場合はFalseを返す

    Parameters
    ----------
    soup : BeautifulSoup
        BeautifulSoupオブジェクト

    Returns
    ----------
    output_temp : dict
        URLの末尾のidをキーとした辞書
    """
    try:
        subscListCards = soup.find("div", class_="subscListCards")
        titles = soup.find_all("div", class_="component-list__title")
        makers = soup.find_all("div", class_="component-list__maker")
        links = subscListCards.find_all("a",)
    except AttributeError as e:
        print("多分全部終わりました…")
        return False
    list_title = [title.get_text() for title in titles]
    list_maker = [maker.get_text() for maker in makers]
    list_link = [urllib.parse.urljoin("https://dlsoft.dmm.co.jp/" ,link.get("href")) for link in links]
    keys = ["title", "maker", "link"]
    output_temp = {
        link.rsplit("/", 1)[-1]: dict(zip(keys, [title, maker, link]))
        for title, maker, link in zip(
            list_title,
            list_maker,
            list_link
        )
    }
    return output_temp


def main():
    HEADERS = {'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              'AppleWebKit/537.36 (KHTML, like Gecko)'
                              'Chrome/100.0.4765.0 Safari/537.36'),}
    p = 1
    output_dic = {}
    while True:
        page = requests.get(base_url + str(p), cookies=dmm_cookie, headers=HEADERS)
        print(f"Getting page:{p}…")
        if page.status_code == 200:
            htmldata = page.text
            soup = BeautifulSoup(htmldata, "html.parser")
            dic_temp = conv_dic(soup)
            if dic_temp:
                output_dic = dict(**output_dic, **dic_temp)
                time.sleep(3)
            else:
                break
        elif page.status_code == 404:
            print("404 response. Exiting…")
            break
        else:
            continue
        p += 1
    os.makedirs("output_json", exist_ok=True)
    with open(r"output_json\dmm_subsc_list_.json", "w") as f:
        json.dump(output_dic, f, indent=4, ensure_ascii=False)
        print("json書き出し完了")
    print("Done.")


def debug():
    with open("dmm_subsc_list_1.html", "r") as f:
        htmldata = f.read()
    soup = BeautifulSoup(htmldata, "html.parser")

    subscListCards = soup.find("div", class_="subscListCards")

    titles = soup.find_all("div", class_="component-list__title")
    makers = soup.find_all("div", class_="component-list__maker")
    links = subscListCards.find_all("a",)

    list_title = [title.get_text() for title in titles]
    list_maker = [maker.get_text() for maker in makers]
    list_link = [urllib.parse.urljoin("https://dlsoft.dmm.co.jp/" ,link.get("href")) for link in links]
    keys = ["title", "maker", "link"]
    output = {
        title: dict(zip(keys, [title, maker, link]))
        for title, maker, link in zip(
            list_title,
            list_maker,
            list_link
        )
    }
    print(output)
    with open("dmm_subsc_list_1.json", "w") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)



if __name__ == "__main__":
    main()
    # debug()