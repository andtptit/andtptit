from cgitb import text
from concurrent.futures import thread
from distutils.log import error
from importlib.resources import path
from tabnanny import check
from time import sleep, time
import requests
import urllib3
import http.client
import random
import datetime
from threading import Thread
import json
from pathlib import Path
import os
import time
import sys

TIMEOUT_IP_CONFIG_SEC = 60
PROXX_URL_FORMAT = 'https://www.proxx.io/proxies.txt?cc={}&user_email=tongvantruong94%40gmail.com&user_token=izgSf2d9G1kL2QNjyKMU'
API_URL = 'https://api.mobrand.net/Gav8vxBSRSOq8drxN7CsGw/bulk/liveoffers/v3/VI9JngfjTJKbkzKgG_yTBQ?apikey=d1FGCEZIcmNiY39BCFRCSH4Hc0N3Rw'

# UPLOAD_URL = 'http://192.168.1.102/api/update_api_mob.php'
UPLOAD_URL = 'http://track.gramgs.com/api/update_api_mob.php'

COUNTRIES_ARRAY = ["us", "jp", "kr", "ru", "in", "sa", "mx", "ca", "th", "tw", "uk"]
TRACKING_ARRAY = ["appsflyer", "adforce", "adjust", "singular", "branch", "kochava"]

NUM_THREAD = 10
IS_RUNNING = False


def get_proxies_by_url(url):
    try:
        response = requests.get(timeout=30, url=url)
        # print(response.status_code)
    except:
        return ''
    return response.text

def get_proxx(geo):
    response = requests.get(timeout=120, url=PROXX_URL_FORMAT.format(geo))
    if(response.status_code == 200):
        print("SUCCESS")

    while response.status_code != 200:
        time.sleep(5)
        print("GETTING PROXY GEO {}".format(geo))
        response = requests.get(timeout=120, url=PROXX_URL_FORMAT.format(geo))
        if(response.status_code == 200):
            print("SUCCESS")

    response = response.text

    try:
        os.remove("{}.txt".format(geo))
    except:
        print("Error while deleting file")
    
    save_file(geo, response)


def get_data_by_file(filename):
    file = open("{}.txt".format(filename),"r", encoding='utf-8')
    counter = 0
    
    Content = file.read()
    return Content

def save_log(name, text):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save = Path('{}.txt'.format(name))
    save.touch(exist_ok=True)
    file = open(save, 'a')

    string_format = "{} - {}\n".format(date, text)

    file.write(string_format)
    file.close()

def save_file(name, text):

    save = Path('{}.txt'.format(name))
    save.touch(exist_ok=True)
    file = open(save, 'a')

    string_format = "{}\n".format(text)

    file.write(string_format)
    file.close()


class CheckOfferThread(Thread):
    def __init__(self, name, headers, proxies, tracking_url, country, platform):
        super(CheckOfferThread, self).__init__()
        self.__name = name
        self.__proxies = proxies
        self.__headers = headers
        self.__tracking_url = tracking_url
        self.__country = country
        self.__platform = platform

    def run(self):
        res_arr = self.__tracking_url
        print("__Start thread {} __ {} __ {}".format(self.__proxies, self.__tracking_url, self.__headers))
        
        # save file used
        save_log('Tracking_used', self.__tracking_url + "|" + self.__country)

        level = 0
        cnt = 0
        try:
            responses = requests.get(self.__tracking_url, headers=self.__headers, proxies=self.__proxies, timeout=TIMEOUT_IP_CONFIG_SEC,  verify=False)
            for response in responses.history:
                res_arr = res_arr + "|" + response.url
                level += 1
                print(response.url)
            print('__________________________')
            print(responses.url)
            res_arr = res_arr + "|" + responses.url
            save_log("Result", res_arr)
            cnt = 3
        except Exception as e:
            print("__ERROR__" + str(e))
            save_log("Result", res_arr)

        pass_tracking = 0
        if "appsflyer" in res_arr or "adjust" in res_arr or "adforce" in res_arr or "singular" in res_arr or "branch" in res_arr or "kochava" in res_arr:
            pass_tracking = 1
        

        data = {
            'country': self.__country,
            'os': self.__platform,
            'data': res_arr,
            'tracking_url': self.__tracking_url,
            'pass_tracking': pass_tracking,
            'level': level
        }

        try:
            res = requests.post(UPLOAD_URL, json=data, timeout=30)
            print('POST SUCCESS')
        except Exception as e:
            pass
        print("__Done thread {}".format(self.__name))


class HandleConfig():
    def __init__(self):
        pass
    
    def __get_tracking(self):
        file = open("Tracking_url.txt","r", encoding='utf-8')

        Content = file.read()
        Content = Content.splitlines()
        return Content

    
    def run(self):
        array_tracking = self.__get_tracking()
        count = 0
        threads = []

        num_loop = int(len(array_tracking) / NUM_THREAD) + 1

        print("NUMBER OF THREADS {}".format(str(NUM_THREAD)))
        print("START LOOP {}".format(str(num_loop)))

        while count < len(array_tracking):

            num_thread = 0
            while num_thread < NUM_THREAD:
                ranx = 0
                proxies_fil = ''
                try:
                    tracking_info = array_tracking[count].split("|")
                    tracking_link = tracking_info[0]
                    proxies_geo = tracking_info[1]
                    platform = tracking_info[2]
                except:
                    exit()

                if (proxies_geo == 'jp'):
                    ranx = random.randint(0, len(proxy_jp) - 1)
                    proxies_fil = proxy_jp[ranx]   

                elif (proxies_geo == 'kr'):
                    ranx = random.randint(0, len(proxy_kr) - 1)
                    proxies_fil = proxy_kr[ranx]

                elif (proxies_geo == 'us'):
                    ranx = random.randint(0, len(proxy_us) - 1)
                    proxies_fil = proxy_us[ranx]

                elif (proxies_geo == 'ru'):
                    ranx = random.randint(0, len(proxy_ru) - 1)
                    proxies_fil = proxy_ru[ranx]

                elif (proxies_geo == 'in'):
                    ranx = random.randint(0, len(proxy_in) - 1)
                    proxies_fil = proxy_in[ranx]

                elif (proxies_geo == 'sa'):
                    ranx = random.randint(0, len(proxy_sa) - 1)
                    proxies_fil = proxy_sa[ranx]

                elif (proxies_geo == 'mx'):
                    ranx = random.randint(0, len(proxy_mx) - 1)
                    proxies_fil = proxy_mx[ranx]

                elif (proxies_geo == 'ca'):
                    ranx = random.randint(0, len(proxy_ca) - 1)
                    proxies_fil = proxy_ca[ranx]

                elif (proxies_geo == 'th'):
                    ranx = random.randint(0, len(proxy_th) - 1)
                    proxies_fil = proxy_th[ranx]

                elif (proxies_geo == 'tw'):
                    ranx = random.randint(0, len(proxy_tw) - 1)
                    proxies_fil = proxy_tw[ranx]
                
                elif (proxies_geo == 'uk'):
                    if (len(proxy_uk) != 0):
                        ranx = random.randint(0, len(proxy_uk) - 1)
                        proxies_fil = proxy_uk[ranx]


                proxies = {
                        'http': 'socks5://' + proxies_fil,
                        'https': 'socks5://' + proxies_fil
                    }
                
                headers = ''
                if (platform == 'ios'):
                    get_user_agent = get_data_by_file('IOS')
                    get_user_agent = get_user_agent.splitlines()
                    ranx = random.randint(0, len(get_user_agent) - 1)
                    user_agent = get_user_agent[ranx]
                    headers = {'user-agent': user_agent}
                else:
                    get_user_agent = get_data_by_file('Android')
                    get_user_agent = get_user_agent.splitlines()
                    ranx = random.randint(0, len(get_user_agent) - 1)
                    user_agent = get_user_agent[ranx]
                    headers = {'user-agent': user_agent}


                filter_thread = CheckOfferThread(str(count+1), headers, proxies, tracking_link, proxies_geo, platform)
                threads.append(filter_thread)
                filter_thread.start()

                count += 1
                num_thread += 1
            
            for filter_thread in threads:
                filter_thread.join()


urllib3.disable_warnings()

num = 0
def get_api_by_url():
    print("START GET TRACKING URL")
    response = requests.get(timeout=120, url=API_URL)
    response = response.json()

    # y = json.loads(response)
    num = 0
    try:
        os.remove("Tracking_url.txt")
    except:
        print("Error while deleting file")

    for key in response['campaigns']:
        for k in key['list']:
            for y in k['countries']:
                for country in COUNTRIES_ARRAY:
                    if y == country:
                        num += 1
                        save_file('Tracking_url', k['offerLink'] + "|" + y + "|" + key['platform'])
    
    print("SUCCESS GET TRACKING URL")


def first_setting():
    print('START GETTING PROXY ...')
    for country in COUNTRIES_ARRAY:
        print('GETTING PROXY GEO {}'.format(country))
        get_proxx(country)
        time.sleep(5)
    
    print("SUCCES GET PROXY")


print('== START RUN: {} =='.format(datetime.datetime.now()))


check_first = sys.argv[1]
get_first_tracking = sys.argv[2]


if(check_first == '1'):
    first_setting()
if(get_first_tracking == '1'):
    get_api_by_url()

print('SETTING FIRST RUN ...')

proxy_jp = []
proxy_kr = []
proxy_us = []
proxy_ru = []
proxy_in = []
proxy_sa = []
proxy_mx = []
proxy_ca = []
proxy_th = []
proxy_tw = []
proxy_uk = []

proxies_jp = get_data_by_file('jp')
proxies_kr = get_data_by_file('kr')
proxies_us = get_data_by_file('us')
proxies_ru = get_data_by_file('ru')
proxies_in = get_data_by_file('in')
proxies_sa = get_data_by_file('sa')
proxies_mx = get_data_by_file('mx')
proxies_ca = get_data_by_file('ca')
proxies_th = get_data_by_file('th')
proxies_tw = get_data_by_file('tw')
proxies_uk = get_data_by_file('uk')

proxies_jp = proxies_jp.splitlines()
proxies_kr = proxies_kr.splitlines()
proxies_us = proxies_us.splitlines()
proxies_ru = proxies_ru.splitlines()
proxies_in = proxies_in.splitlines()
proxies_sa = proxies_sa.splitlines()
proxies_mx = proxies_mx.splitlines()
proxies_ca = proxies_ca.splitlines()
proxies_th = proxies_th.splitlines()
proxies_tw = proxies_tw.splitlines()
proxies_uk = proxies_uk.splitlines()


ran_jp = random.randint(0, len(proxies_jp) - 1)
for i in range(len(proxies_jp) - 1):
    if (proxies_jp[i] != ''):
        proxy_jp.append(proxies_jp[i])

ran_kr = random.randint(0, len(proxies_kr) - 1)
for i in range(len(proxies_kr) - 1):
    if (proxies_kr[i] != ''):
        proxy_kr.append(proxies_kr[i])

ran_us = random.randint(0, len(proxies_us) - 1)
for i in range(len(proxies_us) - 1):
    if (proxies_us[i] != ''):
        proxy_us.append(proxies_us[i])

ran_ru = random.randint(0, len(proxies_ru) - 1)
for i in range(len(proxies_ru) - 1):
    if (proxies_ru[i] != ''):
        proxy_ru.append(proxies_ru[i])

ran_in = random.randint(0, len(proxies_in) - 1)
for i in range(len(proxies_in) - 1):
    if (proxies_in[i] != ''):
        proxy_in.append(proxies_in[i])

ran_sa = random.randint(0, len(proxies_sa) - 1)
for i in range(len(proxies_sa) - 1):
    if (proxies_sa[i] != ''):
        proxy_sa.append(proxies_sa[i])

ran_mx = random.randint(0, len(proxies_mx) - 1)
for i in range(len(proxies_mx) - 1):
    if (proxies_mx[i] != ''):
        proxy_mx.append(proxies_mx[i])

ran_ca = random.randint(0, len(proxies_ca) - 1)
for i in range(len(proxies_ca) - 1):
    if (proxies_ca[i] != ''):
        proxy_ca.append(proxies_ca[i])

ran_th = random.randint(0, len(proxies_th) - 1)
for i in range(len(proxies_th) - 1):
    if (proxies_th[i] != ''):
        proxy_th.append(proxies_th[i])

ran_tw = random.randint(0, len(proxies_tw) - 1)
for i in range(len(proxies_tw) - 1):
    if (proxies_tw[i] != ''):
        proxy_tw.append(proxies_tw[i])

ran_uk = random.randint(0, len(proxies_uk) - 1)
for i in range(len(proxies_uk) - 1):
    if (proxies_uk[i] != ''):
        proxy_uk.append(proxies_uk[i])


HandleConfig().run()