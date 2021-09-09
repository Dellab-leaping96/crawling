import requests
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
import time

#문자열 인트치환
def price_replace(price):
    price=price.replace(',',"")
    price=price.replace("원","")
    price=int(price)
    return price
#db연동하기
mydb = pymysql.connect(
    host="183.111.174.56",
    user="orderhero",
    password="deallab12!",
    database="orderhero"
)
mycursor = mydb.cursor()
#1911879336
productcode=[1911884619,1911872176,1911863547,1911869739,2003400016,1911867473,1911871350,1911872830,
1911867477,1911871263,1911866979,1911893022,1914500898,1911886640,1911872113,1911867296,1911867296,
1911873231,1911882730,1911877283,1911895442,1911869739,1911862861,1914500898,1911858973,1911895392,
1911895759,1911872612,1911886640,1911890768,1911890765,1911886640,1911886639,1911907123,1911886640,
1911886639,1911869555,1911884100,1915100117,1911855567,1915100036,1911857853,1915100091,1911902231,
1911862044,1911902349,1911902380,1921200021,1911868287,1911869799,1911902875,1911902882,1911902901,
1915100022,1915100027,1915100054]
temp=set(productcode)
productcode.clear()
for i in temp:
    productcode.append(i)
prices = [] #가격이들어있는배열
names = [] #상품명 배열

#장보자 크롤링
driver = webdriver.Chrome("/Users/1264/Downloads/chromedriver")
for i in range(len(productcode)):
    url="http://www.jangboja.com/goods/itemDetail?itemCd="+str(productcode[i])+"&unitCd=1"
    driver.get(url)
    driver.implicitly_wait(60)
    time.sleep(1)
    driver.find_element_by_id("itemCnt").send_keys("value",1)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    products_price = soup.find_all(attrs={'id': 'stanPrc'})#할인률이 적용된 가격정보
    products_name = soup.find_all(attrs={'class':'h3-ty1'})   #상품명
    if products_price== []:
        prices.append(0)
        names.append("null")
    else:
        price = products_price[0].get_text().strip()
        name = products_name[0].get_text().strip()
        price = price_replace(price)
        prices.append(price)
        names.append(name)
        print(name)
        print(price)

#table에 값 넣기 (table이 비어있으면 insert 아니라면 update)
for i in range(len(productcode)):
    if(productcode[i]=='1915100027' or productcode[i] == '1911902875'):
        sql = "INSERT INTO TB_CRAWL (SELLER_ID, SELLER_NAME ,CRAWL_CD, NAME, PRICE,CAL,UNIT, REG_DATE) VALUES (%s, %s, %s, %s, %s,NOW())"
        val = ('jbj', '장보자', productcode[i], names[i], prices[i],'*',5)
        mycursor.execute(sql, val)

    else:
        sql = "INSERT INTO TB_CRAWL (SELLER_ID, SELLER_NAME ,CRAWL_CD, NAME, PRICE, REG_DATE) VALUES (%s, %s, %s, %s, %s,NOW())"
        val = ('jbj','장보자' ,productcode[i], names[i], prices[i])
        mycursor.execute(sql, val)

mydb.commit()
