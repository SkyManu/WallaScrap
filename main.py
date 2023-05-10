import datetime
import time  # sleeps

import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

SCROLL_PAUSE_TIME = 5
SLEEP_BETWEEN_CRAWL = 300


def pull_wallapop(url):
    """core function of the script,
it will run in the endless loop"""
    print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: pulling wallapop")
    # some config (else headless driver wont work)
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
    #option.add_argument('--headless')  //No funciona por algun motivo
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

        ) # raspbian
    browser.get(url) # loads page
    browser.implicitly_wait(10) # let it load :)
    try: # apparently not required with headless
        # click on accept cookies
        cookies = browser.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div/div/button").click()
        #print(cookies)
        '''browser.find_element_by_xpath(
            '//*[@id="onetrust-accept-btn-handler"]'
            ).click()'''
    except:
        print('xpath button not found')
        pass

    time.sleep(SCROLL_PAUSE_TIME+np.random.random())
    # adding some randomness in our timings might help us not being detected as a bot

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")
    iter = 0
    print('starting scrolldown loop')
    while True: # loop til there are no more page to scrolldown/load more products

        cheight = browser.execute_script("return document.body.scrollHeight")
        browser.execute_script(f"window.scrollTo(0, {cheight-1000});")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME+np.random.random())
        try:
            moreP = browser.find_element(By.XPATH, "/html/body/tsl-root/tsl-public/div/div/tsl-search/div/tsl-search-layout/div/div[2]/div/div[2]/tsl-button/button").click()
            '''browser.find_elemenet_by_xpath('//*[@id="btn-load-more"]/button').click() # clicks on "more products" button'''

            print((f"{datetime.datetime.now().strftime('%H:%M:%S')}: "
            "clicked in more products already"))
            time.sleep(SCROLL_PAUSE_TIME+np.random.random())
        except:
            print((f"{datetime.datetime.now().strftime('%H:%M:S')}: "
            "'click more products' not found in iter {iter}"))
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            pass

        try:
            soup = BeautifulSoup(browser.page_source, "html.parser")





        except:
            print("error al guardar el item")
            pass

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print(f'breaking at iter {iter} in no more scrolldown/height')
            break
        last_height = new_height
        iter += 1
        if iter > 1 :
            break
    # use beautifulsoup to digest resulting page
    soup = BeautifulSoup(browser.page_source, "html.parser")
    results = soup.find_all("a", class_="ItemCardList__item ng-star-inserted")
    print(results[0])
    #w1 = Wallaitem(results[0].title,"prueba",0)
    #print(w1)





    browser.quit() # quit chrome/chromium
    print(results)



url = 'https://es.wallapop.com/app/search?category_ids=12900&keywords=play%204&latitude=40.02195&longitude=-0.27824&filters_source=quick_filters'
#req = requests.get(url)
#soup = BeautifulSoup(req.text, "lxml")


#print(page.text)
'''def GetItems(soup):
    try:
        elem= browser.find_element(By.XPATH,"/html/body/tsl-root/tsl-public/div/div/tsl-search/div/tsl-search-layout/div/div[2]/div/tsl-public-item-card-list/div/a[1]")


    except:
        pass'''
