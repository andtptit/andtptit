from re import A
import requests


proxies = '163.172.186.190:10035'
user_agent_ios = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/90.0.4430.216 Mobile/15E148 Safari/604.1'
user_agent_android = 'Mozilla/5.0 (Linux; Android 10; SCV41 Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.60 Mobile Safari/537.36'

__url = 'http://avazunew.fusetracking.com/tl?id=eU2HKW2XD3xMgT25eN4QeW4UgTuwD3jUKWGRmG-0N-0N&trafficsourceid=36429'

__headers = {'user-agent': user_agent_android}

__proxy = {
        'http': 'socks5://' + proxies,
        'https': 'socks5://' + proxies
    }


# try:
#     responses = requests.get(__url, headers=__headers, proxies=__proxy, timeout=30,  verify=False)
#     res_arr = ''
#     for response in responses.history:
#         res_arr = res_arr + "|" + response.url
#         print(response.url)
#     print("________________________________")
#     print(responses.url)
# except Exception as e:
#     print("ERROR >>>" + str(e))

a = 1

def xxx():
    global a
    a = 2

xxx()
print(a)