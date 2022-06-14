from concurrent.futures import thread
import requests
import urllib3
import http.client
import random
import datetime
from threading import Thread

TIMEOUT_IP_CONFIG_SEC = 20
PROXX_URL_FORMAT = 'https://www.proxx.io/proxies.txt?cc={}&user_email=tongvantruong94%40gmail.com&user_token=izgSf2d9G1kL2QNjyKMU'


def get_proxies_by_url(url):
    try:
        response = requests.get(timeout=30, url=url)
        # print(response.status_code)
    except:
        return ''
    return response.text


def get_comment_by_file():
    file = open("./File/comment.txt","r", encoding='utf-8')
    counter = 0
    
    Content = file.read()
    CoList = Content.split("\n")
    i = 0
    for i in CoList:
        if i:
            counter += 1

    with open('./File/comment.txt', 'r', encoding='utf-8') as fin:
        data = fin.read().splitlines(True)
    
    ran = random.randint(0, counter - 1)
    return data[ran]

def save_log(text):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    save_log = Path('./File/log.txt')
    save_log.touch(exist_ok=True)
    file = open(save_log, 'a')

    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    text_log = "{} - {}".format(date,text)

    file.write(text_log)
    file.close()

class CheckOfferThread(Thread):
    def __init__(self, name, headers, proxies):
        super(CheckOfferThread, self).__init__()
        self.__name = name
        self.__proxies = proxies
        self.__headers = headers

    def run(self):
        print("__Start thread {}".format(self.__name))
        responses = requests.get('http://track.gramgs.com/checklive.php?aff_id=153&id_offer=3877', headers=self.__headers, proxies=self.__proxies, verify=False)
        for response in responses.history:
            print(response.url)
        print("__Done thread {}".format(self.__name))


class HandleConfig():
    def __init__(self, geo, tracking_url):
        self.__geo = geo
        self.__tracking_url = tracking_url

    def __config_proxies(self):
        url = PROXX_URL_FORMAT.format(self.__geo)
        response = requests.get(timeout=60, url=url)
        response = response.text

        proxies_split = response.splitlines()
        ran = random.randint(0, len(proxies_split) - 1)
        proxies = proxies_split[ran]

        return proxies
    
    def run(self):
        headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; SM-J727S Build/M1AJQ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.143 Mobile Safari/537.36'}

        proxiesx = self.__config_proxies()

        proxies = {
                'http': 'socks5://' + proxiesx,
                'https': 'socks5://' + proxiesx
            }
        count = 0
        threads = []
        while count < 5:
            
            filter_thread = CheckOfferThread(str(count+1), headers, proxies)
            threads.append(filter_thread)
            filter_thread.start()

            count += 1

        for filter_thread in threads:
            filter_thread.join()


def run():
    # http.client.HTTPConnection._http_vsn = 10
    # http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
    urllib3.disable_warnings()

    proxies = get_proxies_by_url(PROXX_URL_FORMAT)
    proxies = proxies.splitlines()

    ran = random.randint(0, len(proxies) - 1)

    print(proxies[ran])

    proxies_ex = {
        'http': 'socks5://' + proxies[ran],
        'https': 'socks5://' + proxies[ran]
    }

    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; SM-J727S Build/M1AJQ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.143 Mobile Safari/537.36'}

    responses = requests.get('http://track.gramgs.com/checklive.php?aff_id=153&id_offer=3877', headers=headers, proxies=proxies_ex, verify=False)
    for response in responses.history:
        print(response.url)



urllib3.disable_warnings()

# headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; SM-J727S Build/M1AJQ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.143 Mobile Safari/537.36'}
# proxies = {
#         'http': 'socks5://' + '212.47.248.15:10059',
#         'https': 'socks5://' + '212.47.248.15:10059'
#     }
# count = 0
# threads = []
# while count < 5:
    
#     filter_thread = CheckOfferThread(str(count+1), headers, proxies)
#     threads.append(filter_thread)
#     filter_thread.start()

#     count += 1

# for filter_thread in threads:
#     filter_thread.join()

HandleConfig('jp', 'http://track.gramgs.com/checklive.php?aff_id=153&id_offer=3877').run()
