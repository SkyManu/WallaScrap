from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd


import sys

def main(args):
    print(args)

if __name__ == '__main__':
    main(sys.argv)

## scroll to an element and click [targetEl can be and element or selector] ##
def scrollClick(driverX, targetEl, maxWait=5, scroll2Top=False, printErr=True):
    try:
        xWait = WebDriverWait(driverX, maxWait)
        if isinstance(targetEl, str):
            xWait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,targetEl)))
            targetEl = driverX.find_element(By.CSS_SELECTOR, targetEl)
        xWait.until(EC.element_to_be_clickable(targetEl))
        driverX.execute_script('''
            arguments[0].scrollIntoView(arguments[1]);
        ''', targetEl, bool(scroll2Top)) ## execute js to scroll
        targetEl.click()
    except Exception as e:
        if printErr: print(repr(e), '\nFailed to click', targetEl)


## find a nextSibling of refEl that matches selector [if specified by sel] ##
def selectNextSib(driverX, refEl, sel=False, printError=False):
    sel = sel.strip() if isinstance(sel, str) and sel.strip() else False
    try: ## execute js code to find next card
        return driverX.execute_script('''
            var sibling = arguments[0].nextElementSibling;
            while (sibling && arguments[1]) {
                if (sibling.matches(arguments[1])) break;
                sibling = sibling.nextElementSibling; } 
            return sibling;''', refEl, sel)
    except Exception as e:
        if printError: print(f'Error finding next "{sel}":',repr(e))


## [bs4] extract text or attribute from a tag inside tagSoup ##
def selectGet(tagSoup, selector='', ta='', defaultVal=None):
    el = tagSoup.select_one(selector) if selector else tagSoup
    if el is None: return defaultVal
    return el.get(ta, defaultVal) if ta else el.get_text(' ', strip=True)


## parse product page html and extract product details ##
def getProductDetails(prodPgHtml:str, prodUrl=None):
    pSoup = BeautifulSoup(prodPgHtml.encode('utf-8'))
    detsDiv = pSoup.select_one('div.detail-item')
    detKeys = [
               'category_id', 'is_bulky', 'is_bumped',
               'is_free_shipping_allowed', 'item_id', 'item_uuid',
               'main_image_thumbnail', 'mine', 'sell_price',
               'seller_user_id', 'subcategory_id', 'itle',
               'title']
    pDets = {} if detsDiv is None else {
        k.lstrip('data-').replace('-', '_'): v
        for k, v in sorted(detsDiv.attrs.items(), key=lambda x: x[0])
        if k.lstrip('data-').replace('-', '_') in detKeys
    }
    pDets['description'] = selectGet(pSoup, 'div.card-product-detail-top>p')
    pDets['date_posted'] = selectGet(pSoup, 'div[class$="published"]')
    pDets['views_count'] = selectGet(pSoup, 'i.ico-eye+span')
    pDets['likes_count'] = selectGet(pSoup, 'i.ico-coounter_favourites+span')
    pDets['seller_name'] = selectGet(pSoup, 'h2.card-user-detail-name')
    uLink = selectGet(pSoup, 'a.card-user-right[href]', 'href')
    if uLink: pDets['seller_link'] = urljoin(prodUrl, uLink)

    ### EXTRACT ANY OTHER DETAILS YOU WANT ###

    pDets['product_link'] = prodUrl
    return pDets

# kSearch, maxItems = 'monitor',10 ## adjust as preferred
# csvname = "holapruebas"
# url = f'https://es.wallapop.com/app/search?keywords={"+".join(kSearch.split())}'
# url = f'{url}&filters_source=search_box&latitude=39.46895&longitude=-0.37686'





def takeItems(csvname) :
    itemCt, scrapedLinks, products = 0, [], []  ## initiate
    itemSel, nextItem = 'a.ItemCardList__item[title]', None
    try: nextItem = browser.find_element(By.CSS_SELECTOR, itemSel) ## first card
    except Exception as e: print('No items found:', repr(e))

    while nextItem:
        itemCt += 1 # counter
        cpHtml, cpTxt = '', '' # clear/initiate
        resultsTab = browser.current_window_handle # to go back

        try: # click card -> open new tab -> scrape product details
            cpHtml, cpTxt = nextItem.get_attribute('outerHTML'), nextItem.text
            scrollClick(browser, nextItem) ## click current card
            # add wait ?
            browser.switch_to.window(browser.window_handles[1]) ## go to 2nd tab
            WebDriverWait(browser, 5).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.detail-item'))) ## wait to load details
            pLink = browser.current_url ## product URL
            if pLink not in scrapedLinks: # skip duplicates [just in case]
                products.append(getProductDetails(browser.page_source, pLink))
            scrapedLinks.append(pLink)
        except Exception as e:
            print('!', [itemCt], ' '.join(cpTxt.split()), repr(e)) ## print error
            pSoup = BeautifulSoup(cpHtml.encode('utf-8'), 'lxml')
            products.append({
                'title': selectGet(pSoup, '', 'title'),
                'price': selectGet(pSoup, 'span.ItemCard__price'),
                'errorMsg': f'{type(e)} {e}'
            }) ## [ make do with info in card ]
        #Para hacer csv
        pd.DataFrame(products).to_csv(csvname + '.csv', index=False)

        try: # close all tabs other than results tab
            for w in browser.window_handles:
                if w != resultsTab:
                    browser.switch_to.window(w)
                    browser.close()
                browser.switch_to.window(resultsTab)
        except Exception as e:
            print('Failed to restore results-tab-only window:', repr(e))
            break

    # print('', end=f"\r[{itemCt} of {maxItems}] {' '.join(cpTxt.split())} {repr(e)}")

        if isinstance(maxItems, int):
            if maxItems < itemCt: break

        nextItem = selectNextSib(browser, nextItem, itemSel) # get next result card
kSearch, maxItems = "monitor 27",500
url = f'https://es.wallapop.com/app/search?keywords={"+".join(kSearch.split())}'
url = f'{url}&filters_source=search_box&latitude=39.46895&longitude=-0.37686'

browser = webdriver.Chrome()
browser.get(url)
browser.maximize_window()

scrollClick(browser, 'button[id="onetrust-accept-btn-handler"]') ## accept cookies
scrollClick(browser, 'tsl-button[id="btn-load-more"]') ## load more [then ∞-scroll]

takeItems(str(maxItems)+"_"+kSearch)