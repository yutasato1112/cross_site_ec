# Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Chrome Driver
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep
from urlextract import URLExtract

#メルカリ検索
def mercari_serch(word):
    #ブラウザインスタンス
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")    
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    #検索文字調整
    m_word = word.replace(" ", "%20")
    m_word = m_word.replace("　", "%20")

    #サイトアクセス
    base_url = 'https://jp.mercari.com/search'
    url = base_url + '?keyword=' + word
    driver.get(url)
    sleep(2)

    #要素抽出
    #商品名
    item_name = driver.find_elements(By.CLASS_NAME,"itemName__a6f874a2")
    item_name_list = []
    for name in item_name:
        item_name_list.append(name.text)
    #商品画像
    item_pic = driver.find_elements(By.TAG_NAME,"picture")
    item_pic_list = []
    item_pic_html = []
    for pic in item_pic:
        item_pic_html.append(pic.get_attribute("innerHTML"))
    extractor = URLExtract()
    for pic in item_pic_html:
        item_pic_list.append(extractor.find_urls(pic)[0])
    #商品価格
    item_price = driver.find_elements(By.CLASS_NAME,"number__6b270ca7")
    item_price_list =[]
    for price in item_price:
        tmp = price.text
        item_price_list.append(tmp.replace(',',''))
    #商品リンク
    item_link = driver.find_elements(By.CLASS_NAME,"sc-5c88f7c4-2.unGnm")
    item_link_list = []
    for link in item_link:
        item_link_list.append(link.get_attribute("href"))
    context = {'word' : word,
               'select' : 'mercari',
               'item_num' : len(item_name_list),
               'item_name' : item_name_list,
               'item_pic' : item_pic_list,
               'item_price' : item_price_list,
               'item_link' : item_link_list,
               }
    driver.close()
    return context

#ヤフオク検索
def yahoo_serch(word):
    # ブラウザインスタンス
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    #検索文字調整
    y_word = word.replace(" ", "+")
    y_word = y_word.replace("　", "+")

    #サイトアクセス
    base_url = 'https://auctions.yahoo.co.jp/search/search'
    url = base_url + '?va=rays&is_postage_mode=1&dest_pref_code=13&exflg=1&b=1&n=50&auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&x=0&y=0&p=' + word
    driver.get(url)
    sleep(2)

    #要素抽出
    #商品名
    item_info = driver.find_elements(By.CLASS_NAME,"Product__titleLink.js-browseHistory-add.js-rapid-override")
    item_name_list = []
    for name in item_info:
        item_name_list.append(name.get_attribute('title'))
    #商品画像
    item_pic_list = []
    for pic in item_info:
        item_pic_list.append(pic.get_attribute('data-auction-img'))
    #商品価格
    item_price = driver.find_elements(By.CLASS_NAME,'Product__priceValue.u-textRed')
    item_price_list = []
    for price in item_price:
        tmp = price.text
        tmp = tmp.replace('円','')
        item_price_list.append(tmp.replace(',', ''))
    #商品リンク
    item_link_list = []
    for link in item_info:
        item_link_list.append(link.get_attribute('href'))
    #残り時間
    item_time = driver.find_elements(By.CLASS_NAME, 'Product__time')
    item_time_list=[]
    for time in item_time:
        item_time_list.append(time.text)
        
    context = {'word' : word,
               'select' : 'yahoo',
               'item_num' : len(item_name_list),
               'item_name' : item_name_list,
               'item_pic' : item_pic_list,
               'item_price' : item_price_list,
               'item_link' : item_link_list,
               'item_time' : item_time_list
               }
    driver.close()
    return context

#全検索
def all_serch(word):
    #メルカリ呼び出し
    m_response = mercari_serch(word)
    m_item_name_list = m_response['item_name']
    m_item_pic_list = m_response['item_pic']
    m_item_price_list = m_response['item_price']
    m_item_link_list = m_response['item_link']


    #ヤフオク呼び出し
    y_response = yahoo_serch(word)
    y_item_name_list = y_response['item_name']
    y_item_pic_list = y_response['item_pic']
    y_item_price_list = y_response['item_price']
    y_item_link_list = y_response['item_link']
    y_item_time_list = y_response['item_time']


    #情報統合処理
    total_name = []
    total_pic = []
    total_price = []
    total_link = []
    total_time = []
    total_origin = []
    total_len = len(m_item_name_list) + len(y_item_name_list)
    
    m_count = 0
    y_count = 0
    for i in range(total_len):
        if i % 2 == 0:
            try:
                total_name.append(m_item_name_list[m_count])
                total_pic.append(m_item_pic_list[m_count])
                total_price.append(m_item_price_list[m_count])
                total_link.append(m_item_link_list[m_count])
                total_time.append(None)
                total_origin.append('Mercari')
                m_count += 1
            except:
                continue
        else:
            try:
                total_name.append(y_item_name_list[y_count])
                total_pic.append(y_item_pic_list[y_count])
                total_price.append(y_item_price_list[y_count])
                total_link.append(y_item_link_list[y_count])
                total_time.append(y_item_time_list[y_count])
                total_origin.append('Yahoo Auction')
                y_count += 1
            except:
                continue
            
    context = {'word' : word,
               'select' : 'all',
               'item_num' : total_len,
               'item_name' : total_name,
               'item_pic' : total_pic,
               'item_price' : total_price,
               'item_link' : total_link,
               'item_time' : total_time,
               'origin' : total_origin
               }
    return context
