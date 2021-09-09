import requests
import pymysql
from bs4 import BeautifulSoup



def price_replace(price):
    price=price.replace(',',"")
    price=price.replace("원","")
    price=int(price)
    return price

mydb = pymysql.connect(
    host="183.111.174.56",
    user="orderhero",
    password="deallab12!",
    database="orderhero"
)
mycursor = mydb.cursor()


#product_code 배열 입니다.
productcode=[66618,4497,58829,63756,48173,31696,31699,53797,40395,4248,43510,58204,
             57807,35743,31732,5556,58204,57807,35743,43712,45062,25727,48330,30730,
             60267,45301,58829,50325,52384,55883,8296,45305,20811,48837,45944,50604,
             31732,51216,52851,57828,31733,49006,31879,48296,51253,60467,49733,50012,53152,25606,49840,45155,49786,
             49903,45141,45154,51720,61190,49877,49838,49880,49886,49884,49763]
temp=set(productcode)
productcode.clear()
for i in temp:
    productcode.append(i)
prices = [] #가격이들어있는배열
names = [] #상품명 배열

#식봄 크롤링
for i in range(len(productcode)):
    webpage= requests.get("https://www.foodspring.co.kr/goods/detail/"+str(productcode[i]))
    soup = BeautifulSoup(webpage.content, "html.parser")
    products_price = soup.find_all(attrs={'class':'real-price'}) #할인률이 적용된 가격정보
    products_name = soup.find_all(attrs={'class':'tit'})    #상품명

    if products_price== []:
        prices.append(0)
        names.append("null")
    else:
        price = products_price[0].get_text().strip()
        name = products_name[0].get_text().strip()
        price = price_replace(price)
        prices.append(price)
        names.append(name)

#table에 값 넣기
for i in range(len(productcode)):
    if productcode[i]==4497:
        cal='/'
        unit=24
        sql = "INSERT INTO TB_CRAWL (SELLER_ID, CRAWL_CD, NAME, PRICE, CAL, UNIT) VALUES (%s, %s, %s, %s, %s, %s)"
        val = ('fs',productcode[i], names[i], prices[i], cal, unit)
        mycursor.execute(sql, val)
    else:
        sql = "INSERT INTO TB_CRAWL (SELLER_ID, CRAWL_CD, NAME, PRICE) VALUES (%s, %s, %s, %s)"
        val = ('fs',productcode[i], names[i], prices[i])
        mycursor.execute(sql,val)

<<<<<<< HEAD
#table eachprice 값 업데이트
# sql= "SET SQL_SAFE_UPDATES = 0"
# mycursor.execute(sql)
#
# sql = "UPDATE foodspring SET eachprice= CASE WHEN quantity>1 THEN price/quantity WHEN quantity<1 THEN price+(price/quantity) ELSE price END"
# mycursor.execute(sql)
=======
>>>>>>> cc1072826bcd9f012b16175cf4094635f9b61d02
mydb.commit()
