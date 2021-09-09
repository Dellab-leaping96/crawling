import requests
import pymysql
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def price_replace(price):
    price=price.replace(',',"")
    price=price.replace("원","")
    price=int(price)
    return price

def get_vendor_cd(vendor):
    vendor_cd= vendor.replace('background-image: url("https://content.foodspring.co.kr/vendor/','')
    return vendor_cd
def get_seller_cd(seller_cd_url):
    seller_cd = seller_cd_url.replace('/vendor/detail/','')
    return seller_cd

def ger_prod_cd(prod_url):
    prod_cd = prod_url.replace('https://www.foodspring.co.kr/goods/detail/','')
    return prod_cd
#db 접속
mydb = pymysql.connect(
    host="183.111.174.56",
    user="orderhero",
    password="deallab12!",
    database="orderhero",
    charset='utf8'
)
mycursor = mydb.cursor()

#식봄에 검색할 키워드 리스트

search_list=['코카콜라 355ml','스프라이트 355ml','서울우유 1L','서울우유 무염버터 450g','생크림 500ml','앵커 무염버터 454g','사세 버팔로윙 1kg','깐마늘(대,소분)1kg',
             '사세 버팔로스틱 1kg','사세 가라아게','홉라 휘핑크림','코다노 모짜렐라AR','스팸 1.81','이츠웰 대두유 18L','해피스푼 대두유 18L','수가 저염베이컨','오뚜기 마요네즈 3.2kg','램웨스턴 냉동감자',
             '매일 휘핑크림','백설 하얀설탕 3kg','백설 하얀설탕 15kg','포마스유','깐양파 1번','깻잎 국내산','다진마늘 중국산','세척당근',
             '대추방울토마토','대파 단','찌개 두부','부추 단','숙주나물','순두부 400g','일반미 20kg', '애호박 인큐', '양배추 국산 망','양파 국산 15kg', '적상추 kg/kg',
             '청상추', '농산물 감자', '팽이버섯 150g']
ms_prod_cd=['P0990005','P0990006','P0410044','P0410039','P0410035','P0410034','P0310010','A0210191','P0310011','P0310153','P0410036','P0410224','P0710034','P0610012',
            'P0610093','P0190041','P0510042','P0110034','P0410094','P0510016','P0510065','P0610066','A0210238','A0210133','A0210229','A0210183','A0110074',
            'A0210199','A9910029','A0210147','A0210217','A9910031','A0310049','A0110157','A0210222','A0210195','A0210168','A0210171','A0210188','A9910016']

print(len(search_list))
print(len(ms_prod_cd))

detail_url_list=[]

# detail_url_list = ['https://www.foodspring.co.kr/goods/detail/4493','https://www.foodspring.co.kr/goods/detail/59834' , 'https://www.foodspring.co.kr/goods/detail/59861', 'https://www.foodspring.co.kr/goods/detail/12271', 'https://www.foodspring.co.kr/goods/detail/4497', 'https://www.foodspring.co.kr/goods/detail/59864', 'https://www.foodspring.co.kr/goods/detail/30817', 'https://www.foodspring.co.kr/goods/detail/59025', 'https://www.foodspring.co.kr/goods/detail/30631', 'https://www.foodspring.co.kr/goods/detail/48173', 'https://www.foodspring.co.kr/goods/detail/63491', 'https://www.foodspring.co.kr/goods/detail/58165', 'https://www.foodspring.co.kr/goods/detail/31696', 'https://www.foodspring.co.kr/goods/detail/53264', 'https://www.foodspring.co.kr/goods/detail/52338', 'https://www.foodspring.co.kr/goods/detail/43502', 'https://www.foodspring.co.kr/goods/detail/31699', 'https://www.foodspring.co.kr/goods/detail/58162', 'https://www.foodspring.co.kr/goods/detail/14861', 'https://www.foodspring.co.kr/goods/detail/4248', 'https://www.foodspring.co.kr/goods/detail/43501', 'https://www.foodspring.co.kr/goods/detail/47037', 'https://www.foodspring.co.kr/goods/detail/36819', 'https://www.foodspring.co.kr/goods/detail/48062', 'https://www.foodspring.co.kr/goods/detail/63602', 'https://www.foodspring.co.kr/goods/detail/65472', 'https://www.foodspring.co.kr/goods/detail/58821', 'https://www.foodspring.co.kr/goods/detail/48342', 'https://www.foodspring.co.kr/goods/detail/63322', 'https://www.foodspring.co.kr/goods/detail/5556', 'https://www.foodspring.co.kr/goods/detail/35666', 'https://www.foodspring.co.kr/goods/detail/25355', 'https://www.foodspring.co.kr/goods/detail/51257', 'https://www.foodspring.co.kr/goods/detail/64319', 'https://www.foodspring.co.kr/goods/detail/25116', 'https://www.foodspring.co.kr/goods/detail/65666', 'https://www.foodspring.co.kr/goods/detail/15497', 'https://www.foodspring.co.kr/goods/detail/15495', 'https://www.foodspring.co.kr/goods/detail/15496', 'https://www.foodspring.co.kr/goods/detail/8502', 'https://www.foodspring.co.kr/goods/detail/11051', 'https://www.foodspring.co.kr/goods/detail/12015', 'https://www.foodspring.co.kr/goods/detail/65054', 'https://www.foodspring.co.kr/goods/detail/53746', 'https://www.foodspring.co.kr/goods/detail/44278', 'https://www.foodspring.co.kr/goods/detail/28978', 'https://www.foodspring.co.kr/goods/detail/65852', 'https://www.foodspring.co.kr/goods/detail/44276', 'https://www.foodspring.co.kr/goods/detail/68804', 'https://www.foodspring.co.kr/goods/detail/51200', 'https://www.foodspring.co.kr/goods/detail/14497', 'https://www.foodspring.co.kr/goods/detail/61105', 'https://www.foodspring.co.kr/goods/detail/74626', 'https://www.foodspring.co.kr/goods/detail/42433', 'https://www.foodspring.co.kr/goods/detail/64832', 'https://www.foodspring.co.kr/goods/detail/52384', 'https://www.foodspring.co.kr/goods/detail/57412', 'https://www.foodspring.co.kr/goods/detail/8296', 'https://www.foodspring.co.kr/goods/detail/10976', 'https://www.foodspring.co.kr/goods/detail/42440', 'https://www.foodspring.co.kr/goods/detail/14413', 'https://www.foodspring.co.kr/goods/detail/25298', 'https://www.foodspring.co.kr/goods/detail/57971', 'https://www.foodspring.co.kr/goods/detail/66562', 'https://www.foodspring.co.kr/goods/detail/46414', 'https://www.foodspring.co.kr/goods/detail/37469', 'https://www.foodspring.co.kr/goods/detail/25299', 'https://www.foodspring.co.kr/goods/detail/42443', 'https://www.foodspring.co.kr/goods/detail/14399', 'https://www.foodspring.co.kr/goods/detail/28688', 'https://www.foodspring.co.kr/goods/detail/5557', 'https://www.foodspring.co.kr/goods/detail/66541', 'https://www.foodspring.co.kr/goods/detail/25190', 'https://www.foodspring.co.kr/goods/detail/25194', 'https://www.foodspring.co.kr/goods/detail/49733', 'https://www.foodspring.co.kr/goods/detail/50011', 'https://www.foodspring.co.kr/goods/detail/50012', 'https://www.foodspring.co.kr/goods/detail/48028', 'https://www.foodspring.co.kr/goods/detail/64124', 'https://www.foodspring.co.kr/goods/detail/63636', 'https://www.foodspring.co.kr/goods/detail/25610', 'https://www.foodspring.co.kr/goods/detail/25609', 'https://www.foodspring.co.kr/goods/detail/25606', 'https://www.foodspring.co.kr/goods/detail/74692', 'https://www.foodspring.co.kr/goods/detail/49839', 'https://www.foodspring.co.kr/goods/detail/49840', 'https://www.foodspring.co.kr/goods/detail/38137', 'https://www.foodspring.co.kr/goods/detail/40255', 'https://www.foodspring.co.kr/goods/detail/38129', 'https://www.foodspring.co.kr/goods/detail/40247', 'https://www.foodspring.co.kr/goods/detail/49903', 'https://www.foodspring.co.kr/goods/detail/49846', 'https://www.foodspring.co.kr/goods/detail/30130', 'https://www.foodspring.co.kr/goods/detail/64302', 'https://www.foodspring.co.kr/goods/detail/51720', 'https://www.foodspring.co.kr/goods/detail/15634', 'https://www.foodspring.co.kr/goods/detail/15266', 'https://www.foodspring.co.kr/goods/detail/29278', 'https://www.foodspring.co.kr/goods/detail/49877', 'https://www.foodspring.co.kr/goods/detail/64842', 'https://www.foodspring.co.kr/goods/detail/49876', 'https://www.foodspring.co.kr/goods/detail/64837', 'https://www.foodspring.co.kr/goods/detail/49880', 'https://www.foodspring.co.kr/goods/detail/49907', 'https://www.foodspring.co.kr/goods/detail/49864', 'https://www.foodspring.co.kr/goods/detail/49886', 'https://www.foodspring.co.kr/goods/detail/49862', 'https://www.foodspring.co.kr/goods/detail/49898', 'https://www.foodspring.co.kr/goods/detail/49884', 'https://www.foodspring.co.kr/goods/detail/49899', 'https://www.foodspring.co.kr/goods/detail/49910', 'https://www.foodspring.co.kr/goods/detail/49851', 'https://www.foodspring.co.kr/goods/detail/49875', 'https://www.foodspring.co.kr/goods/detail/49763']

#페이지 안나오는것들 'https://www.foodspring.co.kr/goods/detail/59834' ,https://www.foodspring.co.kr/goods/detail/60467, https://www.foodspring.co.kr/goods/detail/63943, https://www.foodspring.co.kr/goods/detail/64847 'https://www.foodspring.co.kr/goods/detail/45149' 'https://www.foodspring.co.kr/goods/detail/45130' https://www.foodspring.co.kr/goods/detail/45159 https://www.foodspring.co.kr/goods/detail/45154 https://www.foodspring.co.kr/goods/detail/45161 https://www.foodspring.co.kr/goods/detail/45174

driver = webdriver.Chrome()
driver.implicitly_wait(3)

for search_text,product_code in zip(search_list,ms_prod_cd):
    driver.implicitly_wait(3)
    driver.get('https://www.foodspring.co.kr/search/goods?key='+search_text)
    parent_product=driver.find_element_by_id('productList')
    child_pooducts = parent_product.find_elements_by_class_name('jsClickGoods')

    print(search_text)
    print(product_code)
    #상품코드 가져오기
    for product in child_pooducts:
        driver.implicitly_wait(3)
        a = product.get_attribute('href')
        vendor=product.find_element_by_class_name('img')
        b=vendor.get_attribute('style')
        print(ger_prod_cd(a),get_vendor_cd(b))
        detail_url_list.append(a)

    print('---------------------------------------------------')

for i in range(len(detail_url_list)) :
    driver.implicitly_wait(3)
    driver.get(detail_url_list[i])
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    seller_cd_url = soup.find(attrs={'class':'stroe-name'}).find("a",recursive=False)['href']
    seller_cd_tag = soup.find(attrs={'class': 'stroe-name'}).find("a", recursive=False)
    prods_price = soup.find_all(attrs={'class':'real-price'})
    prods_name = soup.find_all(attrs={'class':'tit'})
    delivery_fees = soup.find(attrs={'class':'delivery-info'}).find_all('dl')
    delivery_fee = delivery_fees[1].findChildren()[1].text
    seller_code = get_seller_cd(seller_cd_url)
    seller_name = seller_cd_tag.get_text().strip()
    price = prods_price[0].get_text().strip()
    price=price_replace(price)
    name = prods_name[0].get_text().strip()
    prod_cd = ger_prod_cd(detail_url_list[i])
    print(prod_cd)
    print(price)
    print(name)
    print("seller_cd"+seller_code)
    print(seller_name)
    print(delivery_fee)
    print('--------------------------')
    cal=''
    unit=''

    if (prod_cd=='25606' or prod_cd=='38129'  or prod_cd=='38137'  or prod_cd=='40247'  or prod_cd=='40255'
            or prod_cd == '49846'  or prod_cd=='49877'  or prod_cd=='49903'  or prod_cd=='50011'  or prod_cd=='53746'):
        cal='*'
        if prod_cd=='25606':
            unit=0.75
        elif prod_cd=='38129' or prod_cd=='38137'  or prod_cd=='40247'  or prod_cd=='40255':
            unit=10
        elif prod_cd == '49846' or prod_cd=='49903':
            unit=2
        elif prod_cd=='49877' or prod_cd=='53746' :
            unit=5
        sql = "INSERT INTO TB_CRAWL (SELLER_ID, SELLER_NAME, CRAWL_CD, NAME, PRICE,CAL,UNIT,DL_FEE, REG_DATE) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
        val = ('fs-' + seller_code, seller_name, prod_cd, name, price, cal, unit, delivery_fee)

        mycursor.execute(sql, val)

    elif(prod_cd=='74626' or prod_cd=='64847'  or prod_cd=='64842'  or prod_cd=='64832'  or prod_cd=='64302'
            or prod_cd == '61105'  or prod_cd=='51200'  or prod_cd=='49910'  or prod_cd=='49899'  or prod_cd=='49898'
            or prod_cd == '49862'  or prod_cd=='45174'  or prod_cd=='45161'  or prod_cd=='45159'  or prod_cd=='45154'
            or prod_cd == '45149'  or prod_cd=='42433'  or prod_cd=='30130'  or prod_cd=='25610'  or prod_cd=='15634'
            or prod_cd == '14497' or prod_cd == '49875' or prod_cd == '49907' or prod_cd =='49864'):
        cal='/'
        if (prod_cd=='45161'):
            unit = 3
        elif (prod_cd=='45154' or prod_cd=='64302' or prod_cd=='30130'):
            unit = 3.5
        elif (prod_cd=='64842' or prod_cd=='49862' or prod_cd=='45174' or prod_cd=='25610' or prod_cd == '49907' or prod_cd =='49864'):
            unit = 4
        elif (prod_cd == '15634'):
            unit = 5
        elif (prod_cd=='49910' or prod_cd=='49899' or prod_cd=='49898' or prod_cd =='49875'):
            unit  = 20
        else:
            unit = 10
        sql = "INSERT INTO TB_CRAWL (SELLER_ID, SELLER_NAME, CRAWL_CD, NAME, PRICE,CAL,UNIT,DL_FEE, REG_DATE) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
        val = ('fs-' + seller_code, seller_name, prod_cd, name, price, cal, unit, delivery_fee)
        mycursor.execute(sql, val)

    else:
        sql = "INSERT INTO TB_CRAWL (SELLER_ID, SELLER_NAME, CRAWL_CD, NAME, PRICE,CAL,UNIT,DL_FEE, REG_DATE) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
        val = ('fs-' + seller_code, seller_name, prod_cd, name, price, cal, unit, delivery_fee)
        mycursor.execute(sql, val)


mydb.commit()

