# Cred to our lab member Xiaohong (Dawn) Yu 'http://cpslab.skku.edu/people-dawnyu.php'

from urllib import request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import selenium
import csv
from selenium import webdriver
import time
import json
from selenium.webdriver.common.keys import Keys

cosmetic = ['키워드 입력'] #리스트 형식으로 다수의 키워드 입력가능; ['노트북','키보드','모니터']


url = 'https://shopping.naver.com/'

driver=webdriver.Chrome() #change the path where your 'chromedriver.exe' locate
driver.implicitly_wait(5)
# driver.maximize_window()
    
print(r"connect url")
driver.get(url)

for typen in cosmetic:

    csvFile=open(r'경로지정'+f'{typen}.csv','w+',encoding='utf-8-sig')
    
    urln = 'https://search.shopping.naver.com/search/all?query=' + typen
    driver.get(urln)
    ###### first crawl the brand name ###############
    
    #브랜드 영역 조회후 카테고리+ 클릭
    try:
        toplist = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/div[2]') 
        toplist.find_element_by_css_selector('a.filter_btn_extend__31sOH').click() 
    except:
        pass
    
     #카테고리+ 파싱
    beautifulObj=BeautifulSoup(driver.page_source,features="html.parser")
   
    subobj1 = beautifulObj.select('div.filter_finder_col__3ttPW')
    # print(subobj1)
    # print(len(subobj1))
    try:
        for mm in subobj1:
            ss = mm.select('div.filter_finder_tit__2VCKd')
            for aa in ss:
                # print(aa.get_text())
                text1 = aa.get_text()
                # print(type(text1))
                # print('브랜드접기' == text1.strip())
                if '브랜드접기' == text1.strip():
                    # print(True)
                    slist = mm.select('span.filter_text_over__3zD9c')
                    print(len(slist))
                    for bb in slist:
                        # print(bb.get_text())
                        csvFile.write(f'{bb.get_text()},\n')
    except:
        pass
    
   #########crawl the title of product ######################################################################################
    for pagingindex in range(1,100):

        print(f'now is {pagingindex}')
        if pagingindex == 1:
            # driver.get(urln)  
            print(pagingindex)
        else:
            pagenumber = driver.find_elements_by_css_selector('a.pagination_btn_page__FuJaU') #크롤링이 끝나면 다음페이지로 이동
            bsobj1 = BeautifulSoup(driver.page_source, features= "html.parser")
            pageobj1 = bsobj1.select('a.pagination_btn_page__FuJaU')
            for pagen, button1 in zip(pageobj1,pagenumber):
                print('pagen:',pagen.get_text())
                print(type(pagen.get_text()))
                if pagen.get_text() == str(pagingindex):
                    print('press button')
                    button1.click()
                    time.sleep(0.5)
                    break
        texts =[] 
        print('text')
        while(True):
            
            body = driver.find_element_by_css_selector('body')
            body.send_keys(Keys.PAGE_DOWN)
            
            # html = body.get_attribute('innerHTML')
            bsObj=BeautifulSoup(driver.page_source,features="html.parser")
            mainobj = bsObj.select('div.basicList_title__3P9Q7 > a')  #

            for mm in mainobj:
                
                text = mm.get_text()

                if text not in texts:
                    print(mm.get_text())
                    csvFile.write(f'{mm.get_text()},\n')
                    texts.append(text)
                    flag = 0 
                
                else:
                    pass
                    
            if (len(texts) >= 40 ):
                break
            else:
                flag +=1
            
            if (flag == 5):
                break

      




time.sleep(5)
csvFile.close()
driver.quit()

