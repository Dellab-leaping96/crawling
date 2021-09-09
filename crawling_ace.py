import requests
import pymysql
from bs4 import BeautifulSoup

def price_replace(price):
    price = price.replace(',', "")
    price=int(price)
    return price

mydb = pymysql.connect(
    host="183.111.174.56",
    user="orderhero",
    password="deallab12!",
    database="orderhero"
)
mycursor = mydb.cursor()

productcode=[415,27643,3472,4786,2030,1788,2028,2033,4481,2171,
2154,2155,3832,2168,4481,2171,4678,4678,24055,22675,859,3472,624,684,
641,577,2154,2155,917,2154,2155,1027,1030,2154,2155,27716,
4430,3546,32,21,23,120,44,80,27244,17,27,36,30,118]
temp=set(productcode)
productcode.clear()
for i in temp:
    productcode.append(i)
prices = [] #가격이들어있는배열
names = [] #상품명 배열

#에이스 크롤링
for i in range(len(productcode)):
    webpage= requests.get("https://www.acemall.asia/shop/view.php?index_no="+str(productcode[i]))
    soup = BeautifulSoup(webpage.content, "html.parser")
    products_price = soup.find_all(attrs={'id':'sell_prc_str'}) #할인률이 적용된 가격정보
    products_name = soup.find_all(attrs={'class':'name'})    #상품명

    if products_price== []:
        prices.append(0)
        names.append("null")
    else:
        price = products_price[0].get_text().strip()
        name = products_name[0].get_text().strip()
        price = price_replace(price)
        prices.append(price)
        names.append(name)

for i in range(len(productcode)):
    #24개box인경우
    if productcode[i]==415:
        cal = '/'
        unit = 24
        sql = "INSERT INTO TB_CRAWL (SELLER_ID,SELLER_NAME, CRAWL_CD, NAME, PRICE, CAL, UNIT, REG_DATE) VALUES (%s, %s, %s, %s, %s, %s,%s, NOW())"
        val = ('ace','에이스', productcode[i], names[i], prices[i], cal, unit)
        mycursor.execute(sql, val)
    elif productcode[i]==3832:
        cal = '/'
        unit = 6
        sql = "INSERT INTO TB_CRAWL (SELLER_ID,SELLER_NAME, CRAWL_CD, NAME, PRICE, CAL, UNIT,REG_DATE) VALUES (%s, %s, %s, %s, %s, %s, %s,NOW())"
        val = ('ace','에이스', productcode[i], names[i], prices[i], cal, unit)
        mycursor.execute(sql, val)
    elif productcode[i]==32:
        cal = '/'
        unit = 3
        sql = "INSERT INTO TB_CRAWL (SELLER_ID,SELLER_NAME, CRAWL_CD, NAME, PRICE, CAL, UNIT, REG_DATE) VALUES (%s, %s, %s, %s, %s, %s, %s,NOW())"
        val = ('ace', '에이스', productcode[i], names[i], prices[i], cal, unit)
        mycursor.execute(sql, val)
    elif productcode[i]==17:
        cal = '*'
        unit = 5
        sql = "INSERT INTO TB_CRAWL (SELLER_ID,SELLER_NAME, CRAWL_CD, NAME, PRICE, CAL, UNIT, REG_DATE) VALUES (%s, %s, %s, %s, %s, %s, %s,NOW())"
        val = ('ace', '에이스', productcode[i], names[i], prices[i], cal, unit)
        mycursor.execute(sql, val)
    else:
        sql = "INSERT INTO TB_CRAWL (SELLER_ID,SELLER_NAME, CRAWL_CD, NAME, PRICE ,REG_DATE) VALUES (%s, %s, %s, %s, %s, NOW())"
        val = ('ace', '에이스', productcode[i], names[i], prices[i])
        mycursor.execute(sql, val)

mydb.commit()

