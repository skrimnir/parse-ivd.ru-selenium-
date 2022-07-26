import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import requests
import re
import traceback
import sqlite3



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.132 YaBrowser/22.3.1.892 Yowser/2.5 Safari/537.36'}

options = webdriver.FirefoxOptions()
options.set_preference("general.useragent.override", 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
options.headless = True
s = Service("C:\pywork\Lusi_selenium\geckodriver.exe")
driver = webdriver.Firefox(
    service = s,
    options=options
)

url_ivd = "https://www.ivd.ru/architects"


def get_html(website):
    html_website = requests.get(website, headers=headers)
    return html_website


def get_contaсt(html):
    soup = BeautifulSoup(html, 'html.parser')
    items_a = soup.find_all('a')
    return items_a



def parse():
    dict_resultat = {}
    exception_list = []
    exception_list_2 = []
    try:
        driver.get(url_ivd)
        time.sleep(0.5)
        driver.find_element(By.CLASS_NAME, "disclamer__close").click() #cookie_button
        time.sleep(1)
        try:
            while True:
                driver.find_element(By.CLASS_NAME, 'btn.btn.btn-light.solid.btn-secondary').click() #show_more_button
                time.sleep(1)
        except:
            print("show_more_button no more")
        user_pic_items = driver.find_elements(By.CLASS_NAME, "user-pic__item")
        print(len(user_pic_items))

        for i in range(len(user_pic_items)):
            print(len(dict_resultat))
            user_pic_items[i].location_once_scrolled_into_view
            #driver.execute_script("arguments[0].scrollIntoView();", user_pic_items[i])
            ActionChains(driver) \
                .key_down(Keys.CONTROL) \
                .click(user_pic_items[i]) \
                .key_up(Keys.CONTROL) \
                .perform()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2.5)

            try:
                driver.find_element(By.CLASS_NAME, "icon.icon--web_icon").click() # website
                driver.switch_to.window(driver.window_handles[2])
                time.sleep(2.5)
                website = driver.current_url

                try:
                    html = get_html(website)
                except:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[1])
                    website = driver.current_url
                    html = get_html(website)
                    file_list = get_contaсt(html.text)
                    email_only = ''
                    try:
                        for i in file_list:
                            try:
                                if 'mailto' in i["href"]:
                                    email_only = i["href"]
                                    email_only = email_only[7:]
                            except:
                                continue
                    except Exception as ex:
                        print(ex)
                    dict_resultat[website] = '', email_only
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(2.5)
                    continue
                file_list = get_contaсt(html.text)
                tel_list = ''
                email_list = ''
                try:
                    for i in file_list:
                        try:
                            if 'tel' in i["href"]:
                                o = i.text
                                p = ''.join(c for c in o if c.isdecimal())
                                if p[0:1] == '7':
                                    p = '+' + p
                                if len(p) > 3 and p[-1] == ',':
                                    p = p[:-1]
                                tel_list = p
                        except:
                            pass
                        try:
                            if 'mailto' in i["href"]:
                                email_list = i["href"]
                                email_list = email_list[7:]
                        except:
                            pass
                        dict_resultat[website] = tel_list, email_list
                except KeyError:
                    exception_list.append(website)
                    website_contacts = website + 'contact'
                    html = get_html(website_contacts)
                    file_list = get_contaсt(html.text)
                    tel_list = ''
                    email_list = ''
                    try:
                        for i in file_list:
                            try:
                                if 'tel' in i["href"]:
                                    o = i.text
                                    p = ''.join(c for c in o if c.isdecimal())
                                    if p[0:1] == '7':
                                        p = '+' + p
                                    if len(p) > 3 and p[-1] == ',':
                                        p = p[:-1]
                                    tel_list = p
                            except:
                                pass
                            try:
                                if 'mailto' in i["href"]:
                                    email_list = i["href"]
                                    email_list = email_list[7:]
                            except:
                                pass
                            dict_resultat[website] = tel_list, email_list
                        # print(driver.current_url + ' 1.1')
                    except KeyError:
                        website_contacts = website + 'contacts'
                        html = get_html(website_contacts)
                        file_list = get_contaсt(html.text)
                        tel_list = ''
                        email_list = ''
                        try:
                            for i in file_list:
                                try:
                                    if 'tel' in i["href"]:
                                        o = i.text
                                        p = ''.join(c for c in o if c.isdecimal())
                                        if p[0:1] == '7':
                                            p = '+' + p
                                        if len(p) > 3 and p[-1] == ',':
                                            p = p[:-1]
                                        tel_list = p
                                except:
                                    pass
                                try:
                                    if 'mailto' in i["href"]:
                                        email_list = i["href"]
                                        email_list = email_list[7:]
                                    dict_resultat[website] = tel_list, email_list
                                except:
                                    pass
                        except KeyError:
                            exception_list_2.append(website)
                            continue

                        try:
                            if dict_resultat[website] == ('', ''):
                                soup = BeautifulSoup(html.text, 'html.parser')
                                all_str_at_mail = soup.find_all(string=re.compile('@' and 'mail'))
                                if len(all_str_at_mail) >= 1:
                                    all_str_at_mail = str(all_str_at_mail[0])
                                    all_str_at_mail = all_str_at_mail.split(' ')
                                for i in all_str_at_mail:
                                    if '@' in i and len(i) < 30:
                                        dict_resultat[website] = '', i
                        except KeyError:
                            traceback.print_exc()
                            continue
                try:
                    driver.close()
                    time.sleep(1.5)
                    driver.switch_to.window(driver.window_handles[1])
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(1.5)
                except Exception as ex:
                    traceback.print_exc()
                    print(ex)


            except:
                website = driver.current_url
                html = get_html(website)
                file_list = get_contaсt(html.text)
                email_only = ''
                try:
                    for i in file_list:
                        try:
                            if 'mailto' in i["href"]:
                                email_only = i["href"]
                                email_only = email_only[7:]
                        except:
                            continue
                except Exception as ex:
                    print(ex)
                dict_resultat[website] = '', email_only
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
                continue

    except Exception as ex:
        traceback.print_exc()
        print(ex)

    finally:
        driver.close()
        driver.quit()
        print(dict_resultat, len((dict_resultat)))
    return dict_resultat


def upgreid_db():
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    blacklist_domain = ['houzz.ru', 'gkamen.com','smartsquare.ru','http://www.greatinterior.ru','']
    parse_dic = parse()
    for key in parse_dic:
        web = f'"{key}"'
        domain_split = re.split('/', web)
        domain = domain_split[2]
        if domain[-1] == '"':
            domain = domain[:-1]
        if 'www' in domain:
            domain = domain[4:]
        if domain in blacklist_domain:
            continue
        telephone_and_email = parse_dic[key]
        cursor.execute(f"SELECT domain FROM Buro WHERE site = '{domain}'")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO Buro (site, inst, tel, email, country, mail_date, response_date, domain, request) VALUES ({web}, '', '{telephone_and_email[0]}', '{telephone_and_email[1]}', 'RU', '', '', '{domain}', 'ivd')")
            db.commit()
        else:
            print(f"'repeat!' {web}")
    db.close()


upgreid_db()





