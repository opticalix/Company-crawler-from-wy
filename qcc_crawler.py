# coding=utf-8
from bs4 import BeautifulSoup
import urllib
from html5lib import treebuilders, treewalkers, serializer
import time
import random
import numpy
from selenium import webdriver

class Qichacha_crawler():
    user_agent_list = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
                   "Opera/8.0 (Windows NT 5.1; U; en)",
                   "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
                   "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
                   "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
                   "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
                   "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
                   "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
                   "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                   "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                   "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
                   "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                   "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                   "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                   "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                   "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
                   "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
                   "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
                   "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
                   "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
                   "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
                   'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon/3.0)',
                   "UCWEB7.0.2.37/28/999",
                   "NOKIA5700/ UCWEB7.0.2.37/28/999",
                   "Openwave/ UCWEB7.0.2.37/28/999"]

    def __init__(self,cookie):
        self.cookie = cookie

    def download(self,url):
        head = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                ,'Accept-Language':'zh-CN,zh;q=0.9'
                ,'Cache-Control':'max-age=0'
                ,'Connection':'keep-alive'
                ,'Cookie':'UM_distinctid=15e564377521e5-019a6849687258-e313761-100200-15e564377541b6; _uab_collina=150468582831443588117478; zg_did=%7B%22did%22%3A%20%2215e5643781640a-0fe292f5fcc46-e313761-100200-15e564378179fa%22%7D; PHPSESSID=s94smovisc8otuk3clajafrpe7; _umdata=0712F33290AB8A6D314F85E60E62F2BF87D062C800AC554CDD629E4FF8CDC0944F26A250F37ADFFCCD43AD3E795C914CD45B5C7A3ADA3C1E2484219FF689EB90; hasShow=1; acw_tc=AQAAAO8FXz4LLAUAns54asaCxrss2fnc; CNZZDATA1254842228=2000071625-1504680875-https%253A%252F%252Fwww.baidu.com%252F%7C1516865152; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516857272974%2C%22updated%22%3A%201516867081320%2C%22info%22%3A%201516538321075%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22bf3d057349688cafdde40c649ba3bf2f%22%7D'
                ,'Host':'www.qichacha.com'
                ,'Referer':'http://www.qichacha.com/index_verify?type=companyview&back=/firm_18ba3dae0e2e3d783131e2addd135929.html'
                ,'Upgrade-Insecure-Requests':1
                ,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                }
        aindex = random.randint(0,len(self.user_agent_list)-1)
        head['User-Agent'] = self.user_agent_list[aindex]
        head['Cookie'] = self.cookie
        req = urllib.request.Request(url, headers=head)
        #传入创建好的Request
        response = urllib.request.urlopen(req)
        #request = urllib2.Request(url,headers=head)
        #response = urllib2.urlopen(request)
        #读取响应信息并解码
        html = response.read()
        #print(html)
        #print(tree)
        soup = BeautifulSoup(html,'html5lib')
        #soup=BeautifulSoup(html, "html.parser",from_encoding="iso-8859-1")
        return soup,html
         
    #根据url爬取数据
    def crawl(self,url,save_path1,save_path2,save_path3,save_path4,fialed_path):
        if not url:
            print('请传入正常的url')
            return
        while not Cominfo_text or not soup:
            if try_time>random.randint(5,10):
                with open(fialed_path, mode='a', encoding='utf-8') as f:
                    f.write(url.replace('\n',''))
                    f.write('\n')
                break
            try_time = try_time+1
            soup = self.download(url)
            if not soup:
                try_time_1 = try_time_1+1
                time.sleep(random.randint(1,3))#
                continue
            Cominfo_text = soup.find('section',id="Cominfo")
            Sockinfo_text = soup.find('section',id="Sockinfo")
            Mainmember_text = soup.find('section',id="Mainmember")
            Subcom_text = soup.find('section',id="Subcom")
            time.sleep(random.randint(1,3))#
        Cominfo = []
        try:
            name_text = soup.find('div',class_="row title")#公司名
            faren = Cominfo_text.find('a',class_="bname")#法人
            name = name_text.get_text().replace(' ','').replace('\n','').replace('在业','').replace('曾用名','').replace('存续','')
            Cominfo.append(name)
            Cominfo.append(faren.get_text())
            
            Cominfo_tables = Cominfo_text.find_all('table')
            print(len(Cominfo_tables))
            if len(Cominfo_tables)==2:
                Cominfo_trs = Cominfo_tables[1].find_all('tr')#基本信息,保存在tr里面
                for Cominfo_tr in Cominfo_trs:
                    tag = 1
                    for td in Cominfo_tr.find_all('td'):
                        if tag%2==0:
                            try:
                                Cominfo.append(td.get_text().replace('\n','').replace(' ','').replace('查看地图附近公司',''))
                            except Exception as e:
                                Cominfo.append(',')
                                print (e) 
                                print ('0')
                        tag = tag+1
                print(len(Cominfo))
                with open(save_path1, mode='a', encoding='utf-8') as f:
                    for v in Cominfo:
                        f.write(v)
                        f.write(',')
                    f.write('\n')

            Sockinfo_tables = Sockinfo_text.find_all('table')
            print(len(Sockinfo_tables))
            if len(Sockinfo_tables)==1:
                Sockinfo_trs = Sockinfo_tables[0].find_all('tr')#基本信息,保存在tr里面
                tag = 0
                for Sockinfo_tr in Sockinfo_trs:
                    if tag:
                        Sockinfo = []
                        Sockinfo.append(name)
                        tds = Sockinfo_tr.find_all('td')[-5:]
                        index = 0
                        for td in tds:
                            try:
                                if index==0:
                                    Sockinfo.append(td.find_all('a')[0].get_text())
                                else:
                                    Sockinfo.append(td.get_text().replace('\n','').replace(' ',''))
                            except Exception as e:
                                Sockinfo.append(',')
                                print (e) 
                                print ('0')
                            index=index+1
                        print(len(Sockinfo))
                        with open(save_path2, mode='a', encoding='utf-8') as f:
                            for v in Sockinfo:
                                f.write(v)
                                f.write(',')
                            f.write('\n')
                    tag = tag+1

            Mainmember_tables = Mainmember_text.find_all('table')
            print(len(Mainmember_tables))
            if len(Mainmember_tables)==1:
                Mainmember_trs = Mainmember_tables[0].find_all('tr')#基本信息,保存在tr里面
                tag = 0
                for Mainmember_tr in Mainmember_trs:
                    if tag:
                        Mainmember = []
                        Mainmember.append(name)
                        tds = Mainmember_tr.find_all('td')[-2:]
                        print(tds)
                        index = 0
                        for td in tds:
                            try:
                                if index==0:
                                    Mainmember.append(td.find_all('a')[0].get_text())
                                else:
                                    Mainmember.append(td.get_text().replace('\n','').replace(' ',''))
                            except Exception as e:
                                Mainmember.append(',')
                                print (e) 
                                print ('0')
                            index=index+1
                        print(len(Mainmember))
                        with open(save_path3, mode='a', encoding='utf-8') as f:
                            for v in Mainmember:
                                f.write(v)
                                f.write(',')
                            f.write('\n')
                    tag = tag+1
                    
            Subcom_tables = Subcom_text.find_all('table')
            print(len(Subcom_tables))
            if len(Subcom_tables)==1:
                Subcom_trs = Subcom_tables[0].find_all('tr')#基本信息,保存在tr里面
                for Subcom_tr in Subcom_trs:
                    tag = 1
                    for td in Subcom_tr.find_all('td'):
                        if tag%2==0:
                            try:
                                Subcom = []
                                Subcom.append(name)
                                Subcom.append(td.find('span').get_text().replace('\n','').replace(' ',''))
                                print(len(Subcom))
                                with open(save_path4, mode='a', encoding='utf-8') as f:
                                    for v in Subcom:
                                        f.write(v)
                                        f.write(',')
                                    f.write('\n')
                            except Exception as e:
                                Subcom.append(',')
                                print (e) 
                                print (' line 155')
                        tag = tag+1
        except Exception as e:
            print (e)
            print (' line 158')

    #根据关键字爬取链接
    def getLinks(self,keyword,num):
        print ("开始获取关键词对应链接.....")
        all_links = []
        page_link = 'http://www.qichacha.com/search?key='+urllib.parse.quote(keyword)
        soup,html = self.download(page_link)
        if soup.find('div',class_='text-center regTab m-t-xl'):
            yanzheng = input("请滑动验证条，然后回车")
            page_link = 'http://www.qichacha.com/search?key='+urllib.parse.quote(keyword)
            soup,html = self.download(page_link)
            time.sleep(random.randint(1,3))
        links = soup.find_all('a',class_='ma_h1')[0:num]
        print(links)
        try:
            if len(links):
                for all_links_ele in links:
                    link = all_links_ele.get('href')
                    if link:
                        all_links.append(link)
            else:
                with open('test.html', mode='a', encoding='utf-8') as f:
                    f.write(html.decode(encoding="utf-8"))
        except Exception as e:
            return all_links
        print(len(all_links))
        return all_links
      
    def verify(self):
        head = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                ,'Accept-Language':'zh-CN,zh;q=0.9'
                ,'Cache-Control':'max-age=0'
                ,'Connection':'keep-alive'
                ,'Cookie':'UM_distinctid=15e564377521e5-019a6849687258-e313761-100200-15e564377541b6; _uab_collina=150468582831443588117478; zg_did=%7B%22did%22%3A%20%2215e5643781640a-0fe292f5fcc46-e313761-100200-15e564378179fa%22%7D; PHPSESSID=s94smovisc8otuk3clajafrpe7; _umdata=0712F33290AB8A6D314F85E60E62F2BF87D062C800AC554CDD629E4FF8CDC0944F26A250F37ADFFCCD43AD3E795C914CD45B5C7A3ADA3C1E2484219FF689EB90; hasShow=1; acw_tc=AQAAAO8FXz4LLAUAns54asaCxrss2fnc; CNZZDATA1254842228=2000071625-1504680875-https%253A%252F%252Fwww.baidu.com%252F%7C1516865152; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516857272974%2C%22updated%22%3A%201516867081320%2C%22info%22%3A%201516538321075%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22bf3d057349688cafdde40c649ba3bf2f%22%7D'
                ,'Host':'www.qichacha.com'
                ,'Referer':'http://www.qichacha.com/index_verify?type=companyview&back=/firm_18ba3dae0e2e3d783131e2addd135929.html'
                ,'Upgrade-Insecure-Requests':1
                ,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                }
        # 进入浏览器设置
        options = webdriver.ChromeOptions()
        # 设置中文
        options.add_argument('lang=zh_CN.UTF-8')
        # 更换头部
        options.add_argument('cookie="UM_distinctid=15e564377521e5-019a6849687258-e313761-100200-15e564377541b6; _uab_collina=150468582831443588117478; zg_did=%7B%22did%22%3A%20%2215e5643781640a-0fe292f5fcc46-e313761-100200-15e564378179fa%22%7D; PHPSESSID=s94smovisc8otuk3clajafrpe7; hasShow=1; _umdata=0712F33290AB8A6D314F85E60E62F2BF87D062C800AC554CDD629E4FF8CDC0944F26A250F37ADFFCCD43AD3E795C914CE5B1695BA72319CE9B8F29721E7AB88C; acw_tc=AQAAAKTljDoPNAoAns54aq2w+57HQ3Ax; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516892766676%2C%22updated%22%3A%201516892766681%2C%22info%22%3A%201516538321075%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22bf3d057349688cafdde40c649ba3bf2f%22%7D; CNZZDATA1254842228=2000071625-1504680875-https%253A%252F%252Fwww.baidu.com%252F%7C1516892739"')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get("http://www.qichacha.com/search?key=%E7%9F%A5%E4%B9%8E")
        time.sleep(10)