# coding=utf-8
from qcc_crawler import Qichacha_crawler
import numpy
import sys  
import urllib
import time
import os
from multiprocessing import Pool,Process, Lock, Manager
import math
import random

def long_time_task(index,endIndex,cookie,batch_size=5):
    print(index)
    print(endIndex)
    memory = 0
    crawler = Qichacha_crawler(cookie)
    save_path1 = '工商信息/公司数据.csv'
    save_path2 = '股东信息/公司数据.csv'
    save_path3 = '主要人员/公司数据.csv'
    save_path4 = '分支机构/公司数据.csv'
    with open('Links.txt', 'r') as f:
        data = f.readlines()[index:endIndex]
        batch_num = math.ceil(len(data)/batch_size)
        for i in range(batch_num):
            batch_data = data[i*batch_size:(i+1)*batch_size]
            batch_links = []
            for line in batch_data:
                print(line)
                links = crawler.crawl(line,save_path1,save_path2,save_path3,save_path4,'failedLinks.txt')
                try_time = 0
                while not links and try_time<3:
                    try_time+=1
                    links = crawler.crawl(line,save_path1,save_path2,save_path3,save_path4,'failedLinks.txt')
                if not links:
                    print('在'+str(index+memory)+'处结束了')
                    next = index+memory
                    return next
                memory+=1
                print(index+memory)
            if os.path.exists('links/0-'+str(index+memory-len(batch_links)-1)+'_Links.txt'):
                os.rename('links/0-'+str(index+memory-len(batch_links)-1)+'_Links.txt', 'links/0-'+str(index+memory-1)+'_Links.txt')
            with open('links/0-'+str(index+memory-1)+'_Links.txt', mode='a', encoding='utf-8') as f:
                for link in batch_links:
                    f.write("http://www.qichacha.com"+link)
                    f.write('\n')
    return index+memory


if __name__=='__main__':
    cookies = ['UM_distinctid=15e564377521e5-019a6849687258-e313761-100200-15e564377541b6; _uab_collina=150468582831443588117478; zg_did=%7B%22did%22%3A%20%2215e5643781640a-0fe292f5fcc46-e313761-100200-15e564378179fa%22%7D; PHPSESSID=s94smovisc8otuk3clajafrpe7; _umdata=0712F33290AB8A6D314F85E60E62F2BF87D062C800AC554CDD629E4FF8CDC0944F26A250F37ADFFCCD43AD3E795C914CD45B5C7A3ADA3C1E2484219FF689EB90; hasShow=1; CNZZDATA1254842228=2000071625-1504680875-https%253A%252F%252Fwww.baidu.com%252F%7C1516865152; acw_tc=AQAAABA4+m0VMwoAns54athaI+Tb3G8P; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516857272974%2C%22updated%22%3A%201516868097385%2C%22info%22%3A%201516538321075%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22bf3d057349688cafdde40c649ba3bf2f%22%7D',
               'UM_distinctid=15e564377521e5-019a6849687258-e313761-100200-15e564377541b6; _uab_collina=150468582831443588117478; zg_did=%7B%22did%22%3A%20%2215e5643781640a-0fe292f5fcc46-e313761-100200-15e564378179fa%22%7D; PHPSESSID=s94smovisc8otuk3clajafrpe7; _umdata=0712F33290AB8A6D314F85E60E62F2BF87D062C800AC554CDD629E4FF8CDC0944F26A250F37ADFFCCD43AD3E795C914CD45B5C7A3ADA3C1E2484219FF689EB90; hasShow=1; CNZZDATA1254842228=2000071625-1504680875-https%253A%252F%252Fwww.baidu.com%252F%7C1516865152; acw_tc=AQAAABA4+m0VMwoAns54athaI+Tb3G8P; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516857272974%2C%22updated%22%3A%201516868102847%2C%22info%22%3A%201516538321075%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22bf3d057349688cafdde40c649ba3bf2f%22%7D',
               'UM_distinctid=15e564377521e5-019a6849687258-e313761-100200-15e564377541b6; _uab_collina=150468582831443588117478; zg_did=%7B%22did%22%3A%20%2215e5643781640a-0fe292f5fcc46-e313761-100200-15e564378179fa%22%7D; PHPSESSID=s94smovisc8otuk3clajafrpe7; _umdata=0712F33290AB8A6D314F85E60E62F2BF87D062C800AC554CDD629E4FF8CDC0944F26A250F37ADFFCCD43AD3E795C914CD45B5C7A3ADA3C1E2484219FF689EB90; hasShow=1; CNZZDATA1254842228=2000071625-1504680875-https%253A%252F%252Fwww.baidu.com%252F%7C1516865152; acw_tc=AQAAABA4+m0VMwoAns54athaI+Tb3G8P; acw_sc__=5a69945f9212dec1eee2dba0a0bcb1a160f9c031; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516857272974%2C%22updated%22%3A%201516868861141%2C%22info%22%3A%201516538321075%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22bf3d057349688cafdde40c649ba3bf2f%22%7D',
               'UM_distinctid=15e564377521e5-019a6849687258-e313761-100200-15e564377541b6; _uab_collina=150468582831443588117478; zg_did=%7B%22did%22%3A%20%2215e5643781640a-0fe292f5fcc46-e313761-100200-15e564378179fa%22%7D; PHPSESSID=s94smovisc8otuk3clajafrpe7; _umdata=0712F33290AB8A6D314F85E60E62F2BF87D062C800AC554CDD629E4FF8CDC0944F26A250F37ADFFCCD43AD3E795C914CD45B5C7A3ADA3C1E2484219FF689EB90; hasShow=1; CNZZDATA1254842228=2000071625-1504680875-https%253A%252F%252Fwww.baidu.com%252F%7C1516865152; acw_tc=AQAAABA4+m0VMwoAns54athaI+Tb3G8P; acw_sc__=5a69945f9212dec1eee2dba0a0bcb1a160f9c031; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516857272974%2C%22updated%22%3A%201516868940513%2C%22info%22%3A%201516538321075%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22bf3d057349688cafdde40c649ba3bf2f%22%7D',
               'UM_distinctid=15e564377521e5-019a6849687258-e313761-100200-15e564377541b6; _uab_collina=150468582831443588117478; zg_did=%7B%22did%22%3A%20%2215e5643781640a-0fe292f5fcc46-e313761-100200-15e564378179fa%22%7D; PHPSESSID=s94smovisc8otuk3clajafrpe7; _umdata=0712F33290AB8A6D314F85E60E62F2BF87D062C800AC554CDD629E4FF8CDC0944F26A250F37ADFFCCD43AD3E795C914CD45B5C7A3ADA3C1E2484219FF689EB90; hasShow=1; CNZZDATA1254842228=2000071625-1504680875-https%253A%252F%252Fwww.baidu.com%252F%7C1516881888; acw_tc=AQAAADTuU2mpag0Ans54al3ro0UwjM4z; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516880266690%2C%22updated%22%3A%201516884280118%2C%22info%22%3A%201516538321075%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22bf3d057349688cafdde40c649ba3bf2f%22%7D',
               'UM_distinctid=15e564377521e5-019a6849687258-e313761-100200-15e564377541b6; _uab_collina=150468582831443588117478; zg_did=%7B%22did%22%3A%20%2215e5643781640a-0fe292f5fcc46-e313761-100200-15e564378179fa%22%7D; PHPSESSID=s94smovisc8otuk3clajafrpe7; _umdata=0712F33290AB8A6D314F85E60E62F2BF87D062C800AC554CDD629E4FF8CDC0944F26A250F37ADFFCCD43AD3E795C914CD45B5C7A3ADA3C1E2484219FF689EB90; hasShow=1; CNZZDATA1254842228=2000071625-1504680875-https%253A%252F%252Fwww.baidu.com%252F%7C1516887289; acw_tc=AQAAAMzoKhXrWQkAns54al14oNaPWVpI; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516887985828%2C%22updated%22%3A%201516888093284%2C%22info%22%3A%201516538321075%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22bf3d057349688cafdde40c649ba3bf2f%22%7D',
               'UM_distinctid=15e564377521e5-019a6849687258-e313761-100200-15e564377541b6; _uab_collina=150468582831443588117478; zg_did=%7B%22did%22%3A%20%2215e5643781640a-0fe292f5fcc46-e313761-100200-15e564378179fa%22%7D; PHPSESSID=s94smovisc8otuk3clajafrpe7; hasShow=1; _umdata=0712F33290AB8A6D314F85E60E62F2BF87D062C800AC554CDD629E4FF8CDC0944F26A250F37ADFFCCD43AD3E795C914CE5B1695BA72319CE9B8F29721E7AB88C; acw_tc=AQAAAKTljDoPNAoAns54aq2w+57HQ3Ax; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516892766676%2C%22updated%22%3A%201516892766681%2C%22info%22%3A%201516538321075%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22bf3d057349688cafdde40c649ba3bf2f%22%7D; CNZZDATA1254842228=2000071625-1504680875-https%253A%252F%252Fwww.baidu.com%252F%7C1516892739',
               ]
    cookie_index = random.randint(0,len(cookies)-1)
    if len(sys.argv)<2:
        next = input('请输入起始索引：')
    else:
        next = sys.argv[1]
    print(next)
    failed_time = 0
    while next<10000:
        pre = next
        next =long_time_task(next,next+100,cookies[cookie_index],5)
        print(next)
        if pre==next:
            failed_time+=1
        else:
            failed_time=0
        if failed_time>3:
            cookie_index = random.randint(0,len(cookies)-1)
            time.sleep(random.randint(10,30))#
        if failed_time>7:
            print('最终停在'+str(next))
            #Qichacha_crawler(cookies[cookie_index]).verify()
            break