from logging import currentframe, disable, error
from selenium import webdriver
from selenium.webdriver.common import proxy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
import time
import os.path
from pathlib import Path
import random
import requests
import sys
import tkinter as tk
from tkinter import *
from tkinter.constants import END
from selenium.webdriver.common.action_chains import ActionChains
from threading import Thread,Event
from datetime import datetime
from tkinter import messagebox
import multiprocessing

STORM_URL_FORMAT = "http://ssh.gramgs.com/sock/?token=dcb173d6ecc32d2589f5b548e91d38a0&country=vn&limitone=1"
URL_911_FORMAT =  "http://track.gramgs.com/api/getproxyport911.php?offerid=3081"
DATE_VERSION = 20211002
VERSION = "BETA"
DEFAULT_TIMEOUT = 60
g_MAX_COMMENT = 1

#### Global Define
g_username = ""
g_password = ""
g_host = ""
g_port = ""
g_txt_link = ""
g_code2fa = ""
STOP_THREAD = FALSE


def addlog(text):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    gui.updateProcessLog('log:{} - {}'.format(date,text))

def directproxy():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

def stormproxy():
    global driver
    try:
        response = requests.get(timeout=30, url=STORM_URL_FORMAT)
        proxy = response.text
        gui.updateProcessLog("Storm: Porxy = {}".format(proxy))
    except:
        gui.updateProcessLog("Get storm proxy failed!")
        driver.close()

    # Socks5 Host SetUp:-
    options = webdriver.ChromeOptions() 
    options.add_argument('--proxy-server=socks5://' + proxy)
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

def sshproxy(g_count, host_ssh, total_port_ssh):
    global driver
    # proxy = '127.0.0.1:10000'

    host_ssh = host_ssh
    total_port_ssh = total_port_ssh

    port_ssh = str(1271 + g_count)
    if g_count >= total_port_ssh and g_count < 2*total_port_ssh:
        port_ssh = str(1271 + g_count - total_port_ssh)
    elif g_count >= 2*total_port_ssh and g_count < 3*total_port_ssh:
        port_ssh = str(1271 + g_count - 2*total_port_ssh)

    proxy = str.format("{}:{}",host_ssh, port_ssh)

    gui.updateProcessLog("SSH: Porxy = {}".format(proxy))

    # Socks5 Host SetUp:-
    options = webdriver.ChromeOptions() 
    options.add_argument('--proxy-server=socks5://' + proxy)
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

def proxy911(i):
    global driver

    if i == 0:
        cmd_format = 'cmd /c "cd 911Proxy/ProxyTool && start ProxyAPI.exe -changeproxy/VN -proxyport={}"'.format(g_port)
        gui.updateProcessLog("________________SEND COMMAND X_________________")
        os.system(cmd_format)

    proxy = "{}:{}".format(g_host,g_port)
    # Socks5 Host SetUp:-
    options = webdriver.ChromeOptions() 
    options.add_argument('--proxy-server=socks5://' + proxy)
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

########################################################
####___Handle file Begin___
def getgroupfromfile(line):
    with open('./File/group.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    # with open('./File/group.txt', 'w') as fout:
    #     fout.writelines(data[1:])
    
    # ran = random.randint(0, counter - 1)
    return data[line]

def getcommentfromfile():
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
    print(ran)
    return data[ran]

def getaccfromfile():
    with open('./File/account.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('./File/account.txt', 'w') as fout:
        fout.writelines(data[1:])

    mailused = Path('./File/account_used.txt')
    mailused.touch(exist_ok=True)
    file = open(mailused, 'a')
    file.write(data[0])
    file.close()

    return data[0]

def savelog(text):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    savelog = Path('./File/log.txt')
    savelog.touch(exist_ok=True)
    file = open(savelog, 'a')

    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    textlog = "{} - {}".format(date,text)

    file.write(textlog)
    file.close()
#####___Handle file End___

def test():
    global driver
    driver = webdriver.Chrome()

    driver.get("https://www.facebook.com/groups/nong.san.que.nha")

    # eles = driver.find_elements_by_xpath("//*[contains(@id, 'mount_0_0')]")
    eles = driver.find_elements_by_xpath("//*[contains(@role, 'button')]")

    for e in eles:
        gui.updateProcessLog(e.text)
        if e.text == "Bình luận":
            gui.updateProcessLog("BLXXX")
            e.click()
        gui.updateProcessLog("xxx")

########################################################
####___Facebook support Begin___

def getcode(code):
    # open tab
    gui.updateProcessLog("XXX")
    driver.execute_script("window.open('https://2fa.vn/','_blank')")
    # Load a page 
    # driver.get("https://2fa.vn/")
    driver.switch_to_window(driver.window_handles[1])
    time.sleep(5)
    url = driver.current_url
    gui.updateProcessLog(url)
    gui.updateProcessLog("input secret 2fa")
    try:
        ele = driver.find_element_by_xpath("//*[@id=\"SECRET2FA\"]")
        ele.send_keys(code)
    except:
        gui.updateProcessLog("input 2fa error!")
        driver.close()

    try:
        ele = driver.find_element_by_xpath("//*[@id=\"form_secret\"]/button")
        ele.click()
    except Exception as e:
        gui.updateProcessLog("Error: {}".format(e))
        driver.close()
    
    time.sleep(5)
    try:
        ele = driver.find_element_by_xpath("//*[@id=\"form_secret\"]/button")
        ele.click()
    except Exception as e:
        gui.updateProcessLog("Error: {}".format(e))
        driver.close()
    
    time.sleep(5)

    elem = driver.find_element_by_xpath("//*[contains(@name, 'code')]")
    gui.updateProcessLog(elem.get_attribute("value"))
    return elem.get_attribute("value")
    
def loginfacebook(groupurl, line):
    if line == 0:
        gui.updateProcessLog("LOGIN FACEBOOK")
        driver.set_page_load_timeout(DEFAULT_TIMEOUT)
        try:
            driver.get(groupurl)
        except:
            gui.updateProcessLog("Open time out")
            savelog("Log:_USER={}_GROUP:{}_TIMEOUT_PROXY\n".format(g_username,groupurl))
            driver.close()
            return False
        time.sleep(2)
        
        try:
            ele = driver.find_element_by_xpath("//input[@name='email']")
            gui.updateProcessLog("input user")
            ele.send_keys(g_username)
        except Exception as e:
            gui.updateProcessLog(e)
            savelog("Log:_USER={}_GROUP:{}_ERROR_INPUT_USERNAME\n".format(g_username,groupurl))

        time.sleep(2)
        try:
            ele = driver.find_element_by_xpath("//input[@name='pass']")
            gui.updateProcessLog("input pass")
            ele.send_keys(g_password)
        except Exception as e:
            gui.updateProcessLog(e)
            savelog("Log:_USER={}_GROUP:{}_ERROR_INPUT_PASSWORD\n".format(g_username,groupurl))

        time.sleep(2)
        try:
            ele = driver.find_element_by_xpath("//*[@id=\"login_form\"]/div[2]/div[3]/div/div")
            gui.updateProcessLog("click button login")
            ele.click()
        except Exception as e:
            gui.updateProcessLog(e)
            savelog("Log:_USER={}_GROUP:{}_ERROR_CLICK_BUTTON_LOGIN\n".format(g_username,groupurl))

        time.sleep(3)
        currenturl = driver.current_url
        if "facebook.com/checkpoint/" in currenturl:
            gui.updateProcessLog("get 2fa code")
            code = getcode(g_code2fa)
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
            try:
                ele = driver.find_element_by_xpath("//*[@id=\"approvals_code\"]")
                gui.updateProcessLog("input code")
                ele.send_keys(code)
            except Exception as e:
                gui.updateProcessLog(e)
                savelog("Log:_USER={}_GROUP:{}_ERROR_GETCODE_2FA\n".format(g_username,groupurl))

        time.sleep(3)
        try:
            ele = driver.find_element_by_xpath("//*[@id=\"checkpointSubmitButton\"]")
            gui.updateProcessLog("click button Login")
            ele.click()
        except Exception as e:
            gui.updateProcessLog(e)
            savelog("Log:_USER={}_GROUP:{}_ERROR_SUBMIT_BUTTON\n".format(g_username,groupurl))

        time.sleep(3)
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"checkpointSubmitButton\"]"))
            )
            ele = driver.find_element_by_xpath("//*[@id=\"checkpointSubmitButton\"]")
            gui.updateProcessLog("click button renew")
            ele.click()
        except Exception as e:
            gui.updateProcessLog(e)
            savelog("Log:_USER={}_GROUP:{}_ERROR_SUBMIT_BUTTON\n".format(g_username,groupurl))
        
        flaglogin = 0
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"checkpointSubmitButton\"]"))
            )
            ele = driver.find_element_by_xpath("//*[@id=\"checkpointSubmitButton\"]")
            gui.updateProcessLog("click button confirm login")
            flaglogin = 1
            ele.click()
        except Exception as e:
            gui.updateProcessLog(e)
            savelog("Log:_USER={}_GROUP:{}_ERROR_SUBMIT_BUTTON\n".format(g_username,groupurl))
        if flaglogin == 1:
            gui.updateProcessLog("___Countinue Check Login___")
            time.sleep(3)
            try:
                element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id=\"checkpointSubmitButton\"]"))
                )
                ele = driver.find_element_by_xpath("//*[@id=\"checkpointSubmitButton\"]")
                gui.updateProcessLog("click button Save login")
                ele.click()
            except Exception as e:
                gui.updateProcessLog(e)
                savelog("Log:_USER={}_GROUP:{}_ERROR_SUBMIT_BUTTON\n".format(g_username,groupurl))
            
            time.sleep(3)
            try:
                element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id=\"checkpointSubmitButton\"]"))
                )
                ele = driver.find_element_by_xpath("//*[@id=\"checkpointSubmitButton\"]")
                gui.updateProcessLog("click button Save login #2")
                ele.click()
            except Exception as e:
                gui.updateProcessLog(e)
                savelog("Log:_USER={}_GROUP:{}_ERROR_SUBMIT_BUTTON\n".format(g_username,groupurl))
    else:
        gui.updateProcessLog("Open group #{}".format(line + 1))
        try:
            driver.execute_script("window.open('{}','_blank')".format(groupurl))
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
            time.sleep(5)
        except Exception as e:
            gui.updateProcessLog("__________________{}_______".format(e))
            savelog("Log:_USER={}_GROUP:{}_ERROR_OPEN_GROUP\n".format(g_username,groupurl))

    ########################################################
    ############# Access account first login ###############
    time.sleep(2)
    flagfirstlogin = 0
    gui.updateProcessLog("CHECK FIRST LOGIN ACCOUNT")
    gui.updateProcessLog("Find button Done")
    index = 0
    for index in range(20):
        try:
            eles = driver.find_elements_by_xpath("//*[contains(@role, 'button')]")
            i = 1
            for e in eles:
            # e.click()
                try:
                    txtdone = e.get_attribute("aria-label")
                    if "Done" in txtdone  or "done" in txtdone:
                        try:
                            e.click()
                            gui.updateProcessLog("Click Done Button")
                            time.sleep(5)
                            break
                        except:
                            gui.updateProcessLog("Try click Done button #{}".format(i))
                except:
                    pass
                i += 1
        except:
            pass
        index += 1
        if index == 19:
            break

    gui.updateProcessLog("Find button Next")
    time.sleep(2)
    index = 0
    for index in range(20):
        try:
            eles = driver.find_elements_by_xpath("//*[contains(@role, 'button')]")
            i = 1
            for e in eles:
            # e.click()
                try:
                    txtdone = e.get_attribute("aria-label")
                    if "Next" in txtdone  or "next" in txtdone:
                        try:
                            e.click()
                            gui.updateProcessLog("click Next Button")
                            time.sleep(5)
                            flagfirstlogin = 1
                            break
                        except:
                            # gui.updateProcessLog("Try click Next button #{}".format(i))
                            pass
                except:
                    pass
                i += 1
        except Exception as e:
            gui.updateProcessLog("Account is not the first login")
        index += 1
        if index == 19:
            break

    if flagfirstlogin == 1:
        gui.updateProcessLog("Find button Get Started")
        time.sleep(2)
        for index in range(20):
            try:
                eles = driver.find_elements_by_xpath("//*[contains(@role, 'button')]")
                i = 1
                for e in eles:
                # e.click()
                    try:
                        txtdone = e.get_attribute("aria-label")
                        if "Started" in txtdone  or "started" in txtdone:
                            try:
                                e.click()
                                gui.updateProcessLog("click  Get Started Button")
                                time.sleep(5)
                                break
                            except:
                                gui.updateProcessLog("Try click Get Started button #{}".format(i))
                    except:
                        pass
                    i += 1
            except Exception as e:
                gui.updateProcessLog(e)
            index += 1

    gui.updateProcessLog("Check URL GROUP")
    for i in range(30):
        currenturl = driver.current_url
        if currenturl in groupurl:
            gui.updateProcessLog("Login done!")
            gui.updateProcessLog("Click screen")
            ActionChains(driver).move_by_offset(1, 1).click().perform()
            break
        if i == 29:
            gui.updateProcessLog("login error!")
            savelog("Log:_USER={}_GROUP:{}_OPEN_GROUP_ERROR\n".format(g_username,groupurl))
            driver.close()
            return False
        time.sleep(1)
####___Facebook support End___

## disable
def handlePublicGroup(group_url,index):
    gui.updateProcessLog("Start threading Auto React!")
    time.sleep(30)

    eles_react = driver.find_elements_by_xpath("//span[@class=\" pq6dq46d\"]")
    i = 1
    try:
        j=1
        i=1
        for e in eles_react:
            if i == index:
                gui.updateProcessLog("Start Auto React #".format(i))
                try:
                    gui.updateProcessLog("___Return HOME PAGE")
                    e.send_keys(Keys.HOME)
                    e.send_keys(Keys.HOME)
                    time.sleep(2)
                    e.click()
                except Exception as e:
                    gui.updateProcessLog("__Error:{}".format(e))

                gui.updateProcessLog("____React post #{} done".format(i))
        time.sleep(50)
    except:
        gui.updateProcessLog("Find Button React error!_")
        time.sleep(100)
        # savelog("Log:_USER={}_GROUP:{}_ERROR\n".format(g_username,group_url))
        # driver.close()
        return
    gui.updateProcessLog("____React Done #02!")
    # savelog("Log:_USER={}_GROUP:{}_SUCCESS={}\n".format(g_username,group_url,i))


def handlePrivateGroup(group_url):
    pass

def threadingAutoCommentPublic(group_url,index):
    time.sleep(1)
    i = 1
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@role, 'textbox')]"))
        )
        eles = driver.find_elements_by_xpath("//*[contains(@role, 'textbox')]")
        for e in eles:
            if i == index:
                comment = getcommentfromfile()
                
                time.sleep(1)
                txtlog = "___Comment Post #{}_i={}".format(i,i)
                gui.updateProcessLog("___Return Agruments")
                try:
                    # driver.execute_script("return arguments[0].scrollIntoView(true);", e)
                    pass
                except:
                    pass
                gui.updateProcessLog(txtlog)
                time.sleep(1)
                # e.click()
                try:
                    e.send_keys(comment)
                    time.sleep(1)
                    e.send_keys(Keys.RETURN)
                except Exception as e:
                    gui.updateProcessLog("__Error:{}".format(e))
                gui.updateProcessLog("Comment post #{} done".format(i))
                time.sleep(random.randint(5,6))
                if i == g_MAX_COMMENT:
                    gui.updateProcessLog("Post Comment Done #01!")
                    savelog("Log:_USER={}_GROUP:{}_SUCCESS={}\n".format(g_username,group_url,i))
                    # driver.close()
                    return
            i+=1
    except:
        gui.updateProcessLog("Find textbox comment error")
        savelog("Log:_USER={}_GROUP:{}_ERROR_FIND_TEXTBOX\n".format(g_username,group_url))
        # driver.close()
        return
    # print("Post Comment Done #02!")
    savelog("Log:_USER={}_GROUP:{}_SUCCESS={}\n".format(g_username,group_url,i))
    return

def threadingAutoCommentPrivate(group_url,group_type):
    if "pri" in group_type:
        gui.updateProcessLog("____JOIN GROUP_____")
        time.sleep(5)
        i=0
        flagPrivate1 = 0
        flagPrivate2 = 0
        for i in range(20):
            try:
                element = WebDriverWait(driver, 20).until(
                    # EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'mount_0_0')]"))
                    # EC.presence_of_element_located((By.XPATH, "//*[contains(@role, 'button')]"))
                    EC.presence_of_element_located((By.XPATH, "//*[contains(@dir, 'auto')]"))
                )
            except:
                gui.updateProcessLog("___Find button Join error___")
                # driver.close()
                flagPrivate1 = 1
                # break
            # eles = driver.find_elements_by_xpath("//*[contains(@dir, 'auto')]")
            eles = driver.find_elements_by_xpath("//*[contains(@role, 'button')]")
            i = 1
            for e in eles:
                # e.click()
                try:
                    txtgroup = e.get_attribute("aria-label")
                    if "Group" in txtgroup  or "nhóm" in txtgroup:
                        try:
                            e.click()
                            gui.updateProcessLog("___click join group___")
                            time.sleep(5)
                            driver.refresh()
                            gui.updateProcessLog("___Click screen___")
                            ActionChains(driver).move_by_offset(500, 100).click().perform()
                            time.sleep(5)
                            break
                        except:
                            gui.updateProcessLog("___Try click Join Group #{}".format(i))
                except:
                    pass
                i += 1

        i = 0
        for i in range(20):
            curenturl = driver.current_url
            if group_url in curenturl:
                flagPrivate2 = 1
                gui.updateProcessLog("___Join Group done__")
                break
            i += 1

            if i == 19:
                gui.updateProcessLog("__Join group error___")
                # driver.close
                break

        if flagPrivate2 == 1:
            gui.updateProcessLog("start auto comment")
            time.sleep(2)
            eles = []
            i = 1
            while len(eles) < g_MAX_COMMENT:
                scroll = 0
                gui.updateProcessLog("___Scroll Down")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)

                try:
                    element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(@role, 'textbox')]"))
                    )
                    eles = driver.find_elements_by_xpath("//*[contains(@role, 'textbox')]")
                    j=1
                    for e in eles:
                        comment = getcommentfromfile()
                        if j >= i:
                            time.sleep(1)
                            txtlog = "Comment Post #{}_i={},j={}".format(i,i,j)
                            gui.updateProcessLog("___Return Agruments___")
                            try:
                                driver.execute_script("return arguments[0].scrollIntoView(true);", e)
                            except:
                                pass
                            gui.updateProcessLog(txtlog)
                            time.sleep(1)
                            # e.click()
                            try:
                                e.send_keys(comment)
                                e.send_keys(Keys.RETURN)
                            except Exception as e:
                                gui.updateProcessLog("__Error:{}".format(e))
                            gui.updateProcessLog("Comment post #{} done".format(i))
                            time.sleep(random.randint(5,20))
                            i+=1
                            if i == g_MAX_COMMENT:
                                gui.updateProcessLog("Post Comment Done #01!")
                                savelog("Log:_USER={}_GROUP:{}_SUCCESS={}\n".format(g_username,group_url,i))
                                # driver.close()
                                return
                        j+=1
                except:
                    gui.updateProcessLog("Find textbox comment error")
                    savelog("Log:_USER={}_GROUP:{}_ERROR\n".format(g_username,group_url))
                    # driver.close()
                    return
            gui.updateProcessLog("Post Comment Done #02!")
            savelog("Log: user={}_start_group:{}_SUCCESS={}\n".format(g_username,group_url,i))
            return

def threadingAutoLike(group_url,index):
    # print("____Start threading Auto React!")
    time.sleep(3)
    if index == 1:
        gui.updateProcessLog("Return HOME PAGE")
        driver.find_element_by_tag_name('body').send_keys(Keys.HOME)

    time.sleep(2)
    eles_react = driver.find_elements_by_xpath("//span[@class=\" pq6dq46d\"]")
    gui.updateProcessLog("React: length={}___index={}".format(len(eles_react),index))
    # try:

    for e in eles_react:
        gui.updateProcessLog("Start Auto React #{}".format(index))
        try:
            if index > 1:
                gui.updateProcessLog("Return Agruments")
                # driver.execute_script("return arguments[0].scrollIntoView(true);", e)
            time.sleep(2)
            
            e.click()
        except Exception as e:
            gui.updateProcessLog("Error:{}".format(e))
        gui.updateProcessLog("React post #{} done".format(index))
        break

    time.sleep(5)
    # except:
    #     print("Find Button React error!_")
    #     time.sleep(100)
    #     # savelog("Log:_USER={}_GROUP:{}_ERROR\n".format(g_username,group_url))
    #     # driver.close()
    #     return
    if index == g_MAX_COMMENT:
        print("React Done #02!")
        return
    savelog("Log:_USER={}_GROUP:{}_SUCCESS={}\n".format(g_username,group_url,index))
    return

########################################################
########___Main Begin___
def main(line, txtmaxcomment, cbuselink, txtlink, cbreply):
    global driver, g_txt_link
    global g_MAX_COMMENT
    g_MAX_COMMENT = int(txtmaxcomment)
    group = getgroupfromfile(line)
    if "|" not in group:
        gui.updateProcessLog("File/group.txt format error!")
        return False
    group_line = group.split("|")
    group_url = group_line[0]
    group_type = group_line[1]

    gui.updateProcessLog("Start Group: {} - Type: {}".format(group_url,group_type))
    #open random group url
    if loginfacebook(group_url, line) == False:
        return False

    cbuselink_var = cbuselink
    if cbuselink_var == 1:
        g_txt_link = txtlink
        gui.updateProcessLog("Open url: {}".format(g_txt_link))
        try:
            driver.get(g_txt_link)
        except:
            gui.updateProcessLog("Open time out")
            time.sleep(50)
            driver.close()
            return False
        time.sleep(2)
        gui.updateProcessLog("Click to screen")
        ActionChains(driver).move_by_offset(1, 1).click().perform()
        time.sleep(2)
        ActionChains(driver).move_by_offset(500, 100).click().perform()
        gui.updateProcessLog("Return HOME PAGE")
        driver.find_element_by_tag_name('body').send_keys(Keys.HOME)

        gui.updateProcessLog("_Threading auto use post link")
        try:
            eles_react = driver.find_elements_by_xpath("//span[@class=\" pq6dq46d\"]")
            for e in eles_react:
                gui.updateProcessLog("Start Auto React")
                try:		
                    e.click()
                    gui.updateProcessLog("React post done")
                    savelog("Log:_USER={}_GROUP:{}_LIKE_SUCCESS\n".format(g_username,group_url))
                except Exception as e:
                    gui.updateProcessLog("Error:{}".format(e))
                    savelog("Log:_USER={}_GROUP:{}_ERROR_LIKE\n".format(g_username,group_url))
                break
        except:
            gui.updateProcessLog("Liked")
            savelog("Log:_USER={}_GROUP:{}_ERROR_LIKED\n".format(g_username,group_url))
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@role, 'textbox')]"))
            )
            eles = driver.find_elements_by_xpath("//*[contains(@role, 'textbox')]")
            for e in eles:
                comment = getcommentfromfile()
                time.sleep(1)
                txtlog = "___Comment Post"
                gui.updateProcessLog(txtlog)
                time.sleep(1)
                try:
                    e.send_keys(comment)
                    time.sleep(1)
                    e.send_keys(Keys.RETURN)
                except Exception as e:
                    gui.updateProcessLog("__Error:{}".format(e))
                gui.updateProcessLog("Comment Post done")
                savelog("Log:_USER={}_GROUP:{}_COMMENT_POST_DOME\n".format(g_username,group_url))
                time.sleep(random.randint(5,6))
                break
        except:
            gui.updateProcessLog("Find textbox comment error")
            savelog("Log:_USER={}_GROUP:{}_ERROR_COMMENT\n".format(g_username,group_url))
            # driver.close()
        time.sleep(2)

        # reply copmment
        if cbreply == 1:
            gui.updateProcessLog("Start Threading auto Reply Comment")
            gui.updateProcessLog("Return HOME PAGE")
            driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
            time.sleep(1)

            eles = driver.find_elements_by_xpath("//*[contains(@role, 'button')]")
            count_reply_comment = 0
            total_reply_comment = 0

            comment = getcommentfromfile()
            for ele in eles:
                try:
                    ele_text = ele.text
                except:
                    ele_text = "XXX"

                if total_reply_comment < 3:
                    if ele_text == "Phản hồi" or ele_text == "Reply":
                        total_reply_comment += 1
                        gui.updateProcessLog("Reply comment #{}".format(total_reply_comment))
                        time.sleep(2)
                        try:
                            ele.click()
                            gui.updateProcessLog("Send Text Reply Comment XXX")
                            ele.send_keys(comment)
                            time.sleep(1)
                            # ele.send_keys(Keys.RETURN)
                            time.sleep(random.randint(10,20))
                        except:
                            gui.updateProcessLog("Reply comment #{} Error".format(total_reply_comment))
                        time.sleep(2)
            
            savelog("Log:_USER={}_GROUP:{}_REP_COMMENT_SUCCESS={}\n".format(g_username,group_url,total_reply_comment))
                    
        driver.close()
        return

    if "pub" in group_type:
        # eles = driver.find_elements_by_xpath("//*[contains(@role, 'button')]")
        # while len(eles) < g_MAX_COMMENT:
        #     gui.updateProcessLog("Total Eles = {}".format(len(eles)))
        #     gui.updateProcessLog("Scroll")
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(10)
        #     eles = driver.find_elements_by_xpath("//*[contains(@role, 'button')]")
        #     # eles = driver.find_elements_by_xpath("//*[contains(@role, 'textbox')]")

        posts = driver.find_elements_by_xpath("//div[@class=\"du4w35lb k4urcfbm l9j0dhe7 sjgh65i0\"]")

        while len(posts) < g_MAX_COMMENT:
            gui.updateProcessLog("Total Posts = {}".format(len(posts)))
            gui.updateProcessLog("Scroll")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            posts = driver.find_elements_by_xpath("//div[@class=\"du4w35lb k4urcfbm l9j0dhe7 sjgh65i0\"]")


        gui.updateProcessLog("_Start threading auto React!")
        gui.updateProcessLog("_Start threading auto Comment!")
        gui.updateProcessLog("MAX COMMENT = {}".format(g_MAX_COMMENT))
        gui.updateProcessLog("_Start threading auto Reply Comment!")

        for i in range(g_MAX_COMMENT):
            threadingAutoLike(group_url,i+1)
            threadingAutoCommentPublic(group_url,i+1)

        gui.updateProcessLog("Auto Like and Comment Done")

        if cbreply == 1:
            gui.updateProcessLog("Start Threading auto Reply Comment")
            gui.updateProcessLog("Return HOME PAGE")
            driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
            time.sleep(1)

            eles = driver.find_elements_by_xpath("//*[contains(@role, 'button')]")
            count_reply_comment = 0
            total_reply_comment = 0
            comment = getcommentfromfile()
            random_reply = random.randint(0, 2)
            for ele in eles:
                try:
                    ele_text = ele.text
                except:
                    ele_text = "XXX"

                if total_reply_comment > g_MAX_COMMENT:
                    gui.updateProcessLog("Reply Comment Done!")
                    break
                elif ele_text == "Phản hồi" or ele_text == "Reply":
                    print("random reply: {} - Count reply: {}".format(random_reply, count_reply_comment))
                    if count_reply_comment == random_reply:
                        total_reply_comment += 1
                        gui.updateProcessLog("Reply comment #{}".format(count_reply_comment+1))
                        time.sleep(2)
                        try:
                            ele.click()
                            gui.updateProcessLog("Send Text Reply Comment XXX")
                            ele.send_keys(comment)
                            time.sleep(1)
                            # ele.send_keys(Keys.RETURN)
                            time.sleep(20)
                        except:
                            gui.updateProcessLog("Reply comment #{} Error".format(count_reply_comment+1))

                        random_reply += random.randint(1, 3)
                        time.sleep(2)
                    else:
                        count_reply_comment += 1

            savelog("Log:_USER={}_GROUP:{}_REP_COMMENT_SUCCESS={}\n".format(g_username,group_url,total_reply_comment))
        gui.updateProcessLog("Start User {} Done #{}".format(g_username, line+1))
        time.sleep(10)
    if "pri" in group_type:
        gui.updateProcessLog("____JOIN GROUP_____")
        time.sleep(5)
        i=0
        flagPrivate1 = 0
        flagPrivate2 = 0
        for i in range(20):
            try:
                element = WebDriverWait(driver, 20).until(
                    # EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'mount_0_0')]"))
                    # EC.presence_of_element_located((By.XPATH, "//*[contains(@role, 'button')]"))
                    EC.presence_of_element_located((By.XPATH, "//*[contains(@dir, 'auto')]"))
                )
            except:
                gui.updateProcessLog("___Find button Join error___")
                # driver.close()
                flagPrivate1 = 1
                # break
            # eles = driver.find_elements_by_xpath("//*[contains(@dir, 'auto')]")
            eles = driver.find_elements_by_xpath("//*[contains(@role, 'button')]")
            i = 1
            for e in eles:
                # e.click()
                try:
                    txtgroup = e.get_attribute("aria-label")
                    if "Group" in txtgroup  or "nhóm" in txtgroup:
                        try:
                            e.click()
                            gui.updateProcessLog("___click join group___")
                            time.sleep(5)
                            driver.refresh()
                            gui.updateProcessLog("___Click screen___")
                            ActionChains(driver).move_by_offset(500, 100).click().perform()
                            time.sleep(5)
                            break
                        except:
                            gui.updateProcessLog("___Try click Join Group #{}".format(i))
                except:
                    pass
                i += 1

        i = 0
        for i in range(20):
            curenturl = driver.current_url
            if group_url in curenturl:
                flagPrivate2 = 1
                gui.updateProcessLog("___Join Group done__")
                break
            i += 1

            if i == 19:
                gui.updateProcessLog("__Join group error___")
                # driver.close
                break

        if flagPrivate2 == 1:
            gui.updateProcessLog("start auto comment")
            time.sleep(2)
            eles = []
            i = 1
            while len(eles) < g_MAX_COMMENT:
                scroll = 0
                gui.updateProcessLog("___Scroll___")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)

                try:
                    element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(@role, 'textbox')]"))
                    )
                    eles = driver.find_elements_by_xpath("//*[contains(@role, 'textbox')]")
                    j=1
                    for e in eles:
                        comment = getcommentfromfile()
                        if j >= i:
                            time.sleep(1)
                            txtlog = "Comment Post #{}_i={},j={}".format(i,i,j)
                            gui.updateProcessLog("___Return Agruments___")
                            try:
                                driver.execute_script("return arguments[0].scrollIntoView(true);", e)
                            except:
                                pass
                            gui.updateProcessLog(txtlog)
                            time.sleep(1)
                            # e.click()
                            try:
                                e.send_keys(comment)
                                e.send_keys(Keys.RETURN)
                            except Exception as e:
                                gui.updateProcessLog("__Error:{}".format(e))
                            gui.updateProcessLog("Comment post #{} done".format(i))
                            time.sleep(random.randint(5,20))
                            i+=1
                            if i == g_MAX_COMMENT:
                                gui.updateProcessLog("Post Comment Done #01!")
                                savelog("Log:_USER={}_GROUP:{}_SUCCESS={}\n".format(g_username,group_url,i))
                                # driver.close()
                                return
                        j+=1
                except:
                    gui.updateProcessLog("Find textbox comment error")
                    savelog("Log:_USER={}_GROUP:{}_ERROR\n".format(g_username,group_url))
                    # driver.close()
                    return
            gui.updateProcessLog("Post Comment Done #02!")
            savelog("Log: user={}_start_group:{}_SUCCESS={}\n".format(g_username,group_url,i))
            return
        
#########___Main End___



#--------- GUI ----------------
def handleLoop():
    for i in range(5):
        print("Loop 1 is running #{}".format(i+1))
        time.sleep(1)
    

global txtmaxcomment
class GUI(Frame):
    def __init__(self, parent, flag):
        Frame.__init__(self, parent)
        # self.thread_main = None
        self.parent = parent
        self.flag = flag
        if self.flag == 0:
            self.initUI()

    def updateProcessLog(self, text):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        textlog = "{} - {}\n".format(date,text)
        self.T.insert(tk.END, textlog)

    def clear(self):
        self.T.delete(1.0,END)
  
    def initUI(self):
        self.parent.geometry("700x600+300+300")
        self.parent.title("Auto Comment FB ver 1.5")
        self.pack(fill=BOTH, expand=True)

        # Create text widget and specify size.
        self.T = Text(self, height = 10, width = 80, bg = "light cyan")
        
        # Create label
        l = Label(self, text = "Process Log")
        l.config(font =("Courier", 14))
        l.pack()
        self.T.pack()
        self.lbhost = Label(self, text = "Host:", font=('arial',11))
        self.lbport = Label(self, text = "Port:", font=('arial',11))

        self.txthost = Entry(self, bd=2, width=30)
        self.txtport = Entry(self, bd=2, width=30)

        self.lbhost_ssh = Label(self, text = "Host:", font=('arial',11))
        self.lbport_num_ssh = Label(self, text = "Total port:", font=('arial',11))

        default_host_ssh = StringVar(self, value='192.168.1.100')
        default_num_port_ssh = StringVar(self, value='30')
        self.txthost_ssh = Entry(self, textvariable=default_host_ssh,  bd=2, width=30)
        self.txtport_num_ssh = Spinbox(self, from_=0,to=30, textvariable=default_num_port_ssh, wrap=True)

        self.lbmaxcomment = Label(self, text = "Số lượng:", font=('arial',11))
        self.lbmaxcomment.place(x=20, y = 350)

        self.txtmaxcomment = Spinbox(self, from_=0,to=30,textvariable=0,wrap=True, values=10)
        self.txtmaxcomment.place(x=110, y = 350)

        self.cbuselink = tk.IntVar() 

        Button5 = tk.Checkbutton(self, text = "Link:", variable = self.cbuselink, onvalue = 1, offvalue = 0, height = 2, width = 10)
        Button5.place(x=1, y = 390)

        self.txtlink = Entry(self, bd=2, width=80)
        self.txtlink.place(x=100,y=395)

        self.cbreply = tk.IntVar(value=1) 
        self.BtnReply = tk.Checkbutton(self, text = "Random Reply Comment", variable = self.cbreply, onvalue = 1, offvalue = 0, height = 2, width = 25)
        self.BtnReply.place(x=1, y = 435)

        self.lbsetting_time = Label(self, text = "Thời gian chuyển giữa các account (phút):", font=('arial',9))
        self.lbsetting_time.place(x=20, y = 490)

        default_time_min= StringVar(self, value='10')
        default_time_max = StringVar(self, value='20')
        self.lbtime_min = Label(self, text = "Min:", font=('arial',9))
        self.lbtime_min.place(x=20, y = 530)
        self.txttime_min = Entry(self, textvariable=default_time_min,  bd=2, width=15)
        self.txttime_min.place(x=60, y = 530)

        self.lbtime_max = Label(self, text = "Max:", font=('arial',9))
        self.lbtime_max.place(x=170, y = 530)
        self.txttime_max = Entry(self, textvariable=default_time_max,  bd=2, width=15)
        self.txttime_max.place(x=210, y = 530)


        self.cbdirect = IntVar()  
        self.cbstorm = IntVar()  
        self.cb911 = IntVar()
        self.cbssh = IntVar()

        Button1 = Checkbutton(self,  text = "Direct", variable = self.cbdirect, onvalue = 1, offvalue = 0, height = 2, width = 10)
        Button2 = Checkbutton(self, text = "Storm", variable = self.cbstorm, onvalue = 1, offvalue = 0, height = 2, width = 10)
        Button3 = Checkbutton(self, text = "911", variable = self.cb911, onvalue = 1, offvalue = 0, height = 2, width = 10, command=self.show911input)
        Button4 = Checkbutton(self, text = "ssh", variable = self.cbssh, onvalue = 1, offvalue = 0, height = 2, width = 10, command=self.showSSHinput)

        Button1.place(x=250, y= 210)
        Button2.place(x=350, y= 210)
        Button3.place(x=450, y= 210)
        Button4.place(x=550, y= 210)

        # Main button
        # Create button for next text.
        btnstart = Button(self, text = "    Start    ", command=self.runProcess, state = NORMAL, height=1,width=8,font=('arial',15,'bold')).place(x=20, y = 200)
        # btnstart = Button(self, text = "    Start    ", command=__run.update, state = NORMAL, height=1,width=8,font=('arial',15,'bold')).place(x=20, y = 200)
        btnstop = Button(self, text = "    Stop    ", command=self.stopProcess, height=1,width=8,font=('arial',15,'bold')).place(x=20, y = 250)
        # btnstart = Button(self, text = "    Start    ", command=lambda: runTest(), height=1,width=8,font=('arial',15,'bold')).place(x=20, y = 200)
        btnreset = Button(self, text = "    Reset    ", command=self.clear, height=1,width=4,font=('arial',12,'bold')).place(x=150, y = 208)

    def show911input(self):
        if self.cb911.get() == 1:
            self.lbhost.place(x = 250, y = 270)
            self.lbport.place(x = 250, y = 310)
            self.txthost.place(x=300, y=270)
            self.txtport.place(x=300, y=310)
        if self.cb911.get() == 0:
            try:
                self.lbhost.place_forget()
                self.lbport.place_forget()
                self.txthost.place_forget()
                self.txtport.place_forget()
            except Exception as e:
                self.updateProcessLog(e)

    def showSSHinput(self):
        if self.cbssh.get() == 1:
            self.lbhost_ssh.place(x = 300, y = 270)
            self.lbport_num_ssh.place(x = 300, y = 310)
            self.txthost_ssh.place(x=380, y=270)
            self.txtport_num_ssh.place(x=380, y=310)
        if self.cbssh.get() == 0:
            try:
                self.lbhost_ssh.place_forget()
                self.lbport_num_ssh.place_forget()
                self.txthost_ssh.place_forget()
                self.txtport_num_ssh.place_forget()
            except Exception as e:
                self.updateProcessLog(e)

    def runProcess(self):
        self.g_proxy = 'direct'
        global g_proxy
        g_direct = self.cbdirect.get()
        g_storm = self.cbstorm.get()
        g_911 = self.cb911.get()
        g_ssh = self.cbssh.get()

        if g_direct == 1 and g_storm == 0 and g_911 == 0 and g_ssh == 0:
            self.g_proxy = 'direct'
        if g_direct == 0 and g_storm == 1 and g_911 == 0 and g_ssh == 0:
            self.g_proxy = 'storm'
        if g_direct == 0 and g_storm == 0 and g_911 == 1 and g_ssh == 0:
            self.g_proxy = '911'
        if g_direct == 0 and g_storm == 0 and g_911 == 0 and g_ssh == 1:
            self.g_proxy = 'ssh'

        # self.thread_main = multiprocessing.Process(target = handleLoop)
        # self.thread_main.start()

        self.thread_main = Thread(target=self.autoStart)
        self.thread_main.start()
        global STOP_THREAD
        STOP_THREAD = False

    def stopProcess(self):
        driver.close()
        global STOP_THREAD
        STOP_THREAD = True
        
        self.updateProcessLog("Stop")
        # self.thread_main.terminate()

    def update(self):
        tx = self.txtmaxcomment.get()
        if int(tx) > 10:
            self.updateProcessLog(tx)
        self.updateProcessLog("pass")

    # Auto Start __
    def autoStart(self):
        global g_username, g_password, g_code2fa, g_host, g_port, STOP_THREAD, g_proxy
        self.updateProcessLog("-------------------------------------------------------")
        self.updateProcessLog("--------- START AUTO COMMENT VERSION = {}---------".format(VERSION))
        self.updateProcessLog("-------------------------------------------------------")
        g_count = 0

        host_ssh = self.txthost_ssh.get()
        total_port_ssh = int(self.txtport_num_ssh.get())

        cbreply = self.cbreply.get()

        time_wait_min = self.txttime_min.get()
        time_wait_max = self.txttime_max.get()

        while not STOP_THREAD:
            file = open("./File/group.txt","r")
            cntGroup = 0
            Content = file.read()
            CoList = Content.split("\n")
            i = 0
            for i in CoList:
                if i:
                    cntGroup += 1

            if cntGroup == 0:
                gui.updateProcessLog("File/group.txt Error")
                break
            g_sum_line_group = cntGroup
            account = getaccfromfile()
            account_info = account.split("|")
            g_username = account_info[0]
            g_password = account_info[1]
            g_code2fa = account_info[2]

            k = 0
            if "911" in self.g_proxy:
                g_host = self.txthost.get()
                g_port = self.txtport.get()
                self.updateProcessLog(g_host)
                self.updateProcessLog(g_port)
                self.updateProcessLog("___COUNT 911 = {}".format(k))
                proxy911(k)
            if "sto" in self.g_proxy:    
                stormproxy()
            if "dir" in self.g_proxy:
                directproxy()
            if "ssh" in self.g_proxy:    
                sshproxy(g_count, host_ssh, total_port_ssh)

            cbuselink_var = self.cbuselink.get()
            txt_link = self.txtlink.get()
            if cbuselink_var == 1:
                g_sum_line_group = 1

            j = 0
            while j < g_sum_line_group:
                line = j
                gui.updateProcessLog("Total Group = {}".format(g_sum_line_group))
                gui.updateProcessLog("Start Group #{}".format(line+1))
                self.updateProcessLog("Start User: {} - luot: #{}".format(g_username,j+1))
                # handle main
                if main(line, self.txtmaxcomment.get(), cbuselink_var, txt_link, cbreply) == False:
                    j = g_sum_line_group
                self.updateProcessLog("Wait for luot moi...")
                # driver.close()
                time.sleep(10)
                j += 1
                if j >= g_sum_line_group:
                    random_wait = random.randint(int(time_wait_min), int(time_wait_max))
                    gui.updateProcessLog("Start User {} Done, Wait {} minutes for luot moi...".format(g_username, random_wait))
                    driver.close()
                    time.sleep(random_wait*60)

            g_count += 1
            if g_count == 100:
                break

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()
  
    def initUI(self):
        self.parent.title("Auto Facebook Support")
        self.pack(fill=BOTH, expand=True)

        Label(self, text="User Name:").place(x=10, y=10)
        Label(self, text="Password:").place(x=10, y=40)
        
        self.e1 = Entry(self)
        self.e1.place(x=140, y=10)
        
        self.e2 = Entry(self)
        self.e2.place(x=140, y=40)
        self.e2.config(show="*")
        
        Button(self, text="Login", command=self.Ok ,height = 3, width = 13).place(x=10, y=100)
    
    def Ok(self):
        global gui
        uname = self.e1.get()
        password = self.e2.get()
    
        if(uname == "" and password == "") :
            messagebox.showinfo("", "Blank Not allowed")
    
    
        elif(uname.lower() == "admin" and password.lower() == "admin@123"):
            self.destroy()
            gui = GUI(root,0)
    
        else :
            messagebox.showinfo("","Incorrent Username and Password")

root = Tk()
root.geometry("300x180+300+300")
root.iconbitmap('icon.ico')
app = Example(root)
global gui
if __name__ == '__main__':
    root.mainloop()

