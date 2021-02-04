from urllib import request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import selenium
import konlpy
from konlpy.tag import Kkma
import csv
from selenium import webdriver
import time
import json
from selenium.webdriver.common.keys import Keys

cosmetic = ['펫케어'] 
# ,'노트북','키보드','모니터']


url = 'https://shopping.naver.com/'

driver=webdriver.Chrome() #change the path where your 'chromedriver.exe' locate
driver.implicitly_wait(5)
# driver.maximize_window()
    
print(r"connect url")
driver.get(url)

for typen in cosmetic:

    csvFile=open(r'.\datas\반려동물_'+f'{typen}.csv','w+',encoding='utf-8-sig')
    
    urln = 'https://search.shopping.naver.com/search/all?query=' + typen
    driver.get(urln)
    ###### first crawl the brand name ###############
    
    try:
        toplist = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/div[2]')
        toplist.find_element_by_css_selector('a.filter_btn_extend__31sOH').click()
    except:
        pass
    
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
    # toplist1 = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/ul/li[1]/a/span')
    # print(toplist1.get_text())

    # mm = toplist.find_element_by_css_selector('div.filter_finder_cell__2218d')
    # name = mm.find_elements_by_css_selector('span.filter_text_over__3zD9c')
    # print(len(name))
    # for jj in name:
    #     print(jj.get_text())
   #########crawl the title of product ######################################################################################
    for pagingindex in range(1,100):

        print(f'now is {pagingindex}')
        if pagingindex == 1:
            # driver.get(urln)  
            print(pagingindex)
        else:
            # driver.find_element_by_css_selector('input.searchInput_search_input__3ZswN').send_keys('화장품'+f'{typen}')
            # print(urln+ f"&pagingIndex={pagingindex}&pagingSize=40&productSet=total&query=화장품{typen}&sort=rel&timestamp=&viewType=list")
            # urlfollowing = urln+ f"&pagingIndex={pagingindex}&pagingSize=40&productSet=total&query=화장품{typen}&sort=rel&timestamp=&viewType=list"
            # # &pagingSize=40&productSet=total&query=화장품스킨케어&sort=rel&timestamp=&viewType=list
            # # &pagingSize=40&productSet=total&query=화장품스킨케어&sort=rel&timestamp=&viewType=list
            # driver.get(urlfollowing) 
            # print(2)
            # if pagingindex == 3:
            #     time.sleep(1000)
            pagenumber = driver.find_elements_by_css_selector('a.pagination_btn_page__FuJaU')
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
            mainobj = bsObj.select('div.basicList_title__3P9Q7 > a') 

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

