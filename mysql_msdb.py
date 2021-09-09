import requests
import pymysql
from bs4 import BeautifulSoup

def price_replace(price):
    price = price.replace(',', "")
    price=int(price)
    return price

mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="4947",
    database="mydatabase"
)
mycursor= mydb.cursor()
check = "SHOW TABLES LIKE 'TB_MS_CRAWL'"
mycursor.execute(check)
result=mycursor.fetchall()
if len(result) ==1:
    sql="DROP TABLE TB_MS_CRAWL"
    mycursor.execute(sql)
#TABLE 생성
mycursor.execute("CREATE TABLE TB_MS_CRAWL (PROD_CD varchar(10) NOT NULL, SELLER_ID VARCHAR(100) NOT NULL, SELLER_CD INT(11),USE_YN varchar(2) NOT NULL DEFAULT 'Y', REG_DATE DATETIME DEFAULT NOW())")

sql ="select mscode,foodspringcode from msdb;"
mycursor.execute(sql)
myresult1 = mycursor.fetchall()

sql ="select mscode,acecode from msdb;"
mycursor.execute(sql)
myresult2 = mycursor.fetchall()

sql ="select mscode,jangbojacode from msdb;"
mycursor.execute(sql)
myresult3 = mycursor.fetchall()

for x,y,z in zip(myresult1,myresult2,myresult3):
    sql = "INSERT INTO TB_MS_CRAWL (PROD_CD, SELLER_ID, SELLER_CD) VALUES (%s, %s, %s)"
    val = (x[0], "식봄", x[1])
    mycursor.execute(sql, val)
    val = (x[0], "에이스", y[1])
    mycursor.execute(sql, val)
    val = (x[0], "장보자", z[1])
    mycursor.execute(sql, val)
mydb.commit()

