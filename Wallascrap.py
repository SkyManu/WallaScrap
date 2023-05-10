import requests
import lxml
import urllib.request
import time


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver  # browser driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options  # to suppress the browser
from selenium.webdriver import DesiredCapabilities
import datetime
import time  # sleeps
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import demoji
import csv
import tkinter as tk

import Wallaitem

class Wallascrap:
    entradanombre ="reserved"
    url="https://es.wallapop.com/app/search?keywords=monitor%2024%22&filters_source=recent_searches&latitude=39.4788864&longitude=-0.360448"
    veces = 1

    #url = 'https://es.wallapop.com/app/search?category_ids=12900&keywords=play%204&latitude=40.02195&longitude=-0.27824&filters_source=quick_filters'

    #entradanombre = "owo"

    def SetEntradaNombre(self, nuevaentrada):
        Wallascrap.entradanombre = nuevaentrada

    def __SepararEnTuplas(self,lista):
        lista1 = lista[0]
        lista2 = (" ").join(lista[1:])
        res = (lista1, lista2)
        return res

    def pull_wallapop(self, url,profundidad ):
        veces = int(profundidad)
        SCROLL_PAUSE_TIME = 1
        SLEEP_BETWEEN_CRAWL = 300


        # Cosas necesarias para el csv
        Mycsv = open(Wallascrap.entradanombre + ".csv", "a",encoding="utf-8-sig", newline="")
        writer = csv.writer(Mycsv)
        """core function of the script,
    it will run in the endless loop"""
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: pulling wallapop")
        # some config (else headless driver wont work)

        # Tratado de caracteres raros
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        option = Options()

        option.add_argument("--no-sandbox")
        option.add_argument("--window-size=1920x1080")
        option.add_argument("--disable-extensions")
        option.add_argument("--proxy-server='direct://'")
        option.add_argument("--proxy-bypass-list=*")
        option.add_argument("--start-maximized")
        # option.add_argument('--headless')  //No funciona por algun motivo
        option.add_argument('--disable-gpu')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--ignore-certificate-errors')

        # browser = webdriver.Chrome(
        # "./notebooks/chromedriver_win32/chromedriver.exe",
        # options=option, desired_capabilities=capabilities
        # ) # debugging in a windows box
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                   options=option,
                                   desired_capabilities=capabilities

                                   )  # raspbian
        browser.get(url)  # loads page
        browser.implicitly_wait(10)  # let it load :)
        try:  # apparently not required with headless
            # click on accept cookies
            cookies = browser.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div/div/button").click()
            # print(cookies)
            '''browser.find_element_by_xpath(
                '//*[@id="onetrust-accept-btn-handler"]'
                ).click()'''
        except:
            print('xpath button not found')
            pass

        time.sleep(SCROLL_PAUSE_TIME + np.random.random())
        # adding some randomness in our timings might help us not being detected as a bot

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")
        iter = 0
        print('starting scrolldown loop')
        while True:  # loop til there are no more page to scrolldown/load more products

            cheight = browser.execute_script("return document.body.scrollHeight")
            browser.execute_script(f"window.scrollTo(0, {cheight - 1000});")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME + np.random.random())
            try:
                moreP = browser.find_element(By.XPATH,
                                             "/html/body/tsl-root/tsl-public/div/div/tsl-search/div/tsl-search-layout/div/div[2]/div/div[2]/tsl-button/button").click()
                '''browser.find_elemenet_by_xpath('//*[@id="btn-load-more"]/button').click() # clicks on "more products" button'''

                print((f"{datetime.datetime.now().strftime('%H:%M:%S')}: "
                       "clicked in more products already"))
                time.sleep(SCROLL_PAUSE_TIME + np.random.random())
            except:
                print((f"{datetime.datetime.now().strftime('%H:%M:%S')}: "
                       "'click more products' not found in iter {iter}"))
                browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print(f'breaking at iter {iter} in no more scrolldown/height')
                iter = veces+1
                break
            last_height = new_height
            iter += 1
            print(iter)
            if iter > veces:
                break

        if iter > veces:
            try:
                soup = BeautifulSoup(browser.page_source, "html.parser")
                results = soup.find_all("a", class_="ItemCardList__item ng-star-inserted")
                # f = results[12].text
                # arr = f.split()
                #
                # for elem in arr:
                #     try:
                #
                #         if elem == "AnteriorSiguiente":
                #             lalista = arr[arr.index(elem) + 1:]
                #
                #     except:
                #         print("No se esta tratando la string correctamente")
                #
                # print(lalista)




            except:
                print("error al guardar el item")
                pass

            # use beautifulsoup to digest resulting page

            i = 0
            for n in results:
                #Saber si esta reservado o no
                reserved= str(n).find("reserved")
                if reserved > -1:
                    reserved=1

                #Precio y nombre
                aux = demoji.replace(n.text, "")
                aux2=aux.replace('\"',"")
                aux2 = aux.replace('\'', "")
                myarray = aux2.split()
                print("myArray: ", myarray)
                for elemento in myarray:
                    i += 1

                    if elemento == "AnteriorSiguiente":
                        i = 0
                        listadef = myarray[myarray.index(elemento) + 1:]
                        # trueString= (",").join(listadef)
                        # print("trueString: " ,trueString)
                        # file.write(trueString+ '\n')
                        res1 = Wallascrap.__SepararEnTuplas(self,listadef)
                        writer.writerow(res1+ (reserved,))
                        break


                    elif i == len(myarray) - 1:
                        i = 0
                        # anotherString = (',').join(myarray)
                        # print("anotherString : ",anotherString)
                        # file.write(anotherString+'\n')
                        res2 = Wallascrap.__SepararEnTuplas(self,myarray)
                        writer.writerow(res2 + (reserved,))
        # pull_wallapop(url,entradanombre)

        # file.write( demoji.replace(truelista,""))

        # w1 = Wallaitem(results[0].title,"prueba",0)
        # print(w1)

        # req = requests.get(url)
        # soup = BeautifulSoup(req.text, "lxml")

        # print(page.text)

    '''def GetItems(soup):
        try:
            elem= browser.find_element(By.XPATH,"/html/body/tsl-root/tsl-public/div/div/tsl-search/div/tsl-search-layout/div/div[2]/div/tsl-public-item-card-list/div/a[1]")


        except:
            pass'''

















