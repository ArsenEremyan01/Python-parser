import time
import requests
import yaml
from bs4 import BeautifulSoup
from yaml.loader import SafeLoader

box = set()


def load_configs():
    yml = open('configs.yml')
    data = yaml.load(yml, SafeLoader)
    yml.close()
    return data


def make_mess(conf):
    url = conf["URL"]
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    allNews = soup.findAll('a', class_='news_item__title')
    filteredNews = ' '.join([i for i in allNews[0].text.split(' ') if i])
    return filteredNews


def send_mess(conf, news):
    if box:
        for i in box:
            if i != news: pushh(news, conf)
    else:
        pushh(news, conf)

    box.add(news)


def pushh(news, conf):
    token = conf["TOKEN"]  # add TOKEN to configs
    url = conf["API"]
    channel_id = conf["CHANEL_ID"]
    url += token
    method = url + "/sendMessage"
    send_message = requests.post(method, data={
        "chat_id": channel_id,
        "text": news
    })
    print("Отправка записи в телеграм...")

    if send_message.status_code != 200:
        raise Exception("post_text error")


if __name__ == "__main__":
    while True:
        load = load_configs()
        print("Идет добавление конфигураций...")
        make = make_mess(load)
        print("Подготовка записи к отправке...")
        send_mess(load, make)
        time.sleep(10)
