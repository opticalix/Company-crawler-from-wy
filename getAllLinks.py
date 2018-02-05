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
    with open('company_name.txt', 'r') as f:
        data = f.readlines()[index:endIndex]
        batch_num = math.ceil(len(data)/batch_size)
        for i in range(batch_num):
            batch_data = data[i*batch_size:(i+1)*batch_size]
            batch_links = []
            for line in batch_data:
                print(line)
                links = crawler.getLinks(line,1)
                try_time = 0
                while not links and try_time<3:
                    try_time+=1
                    links = crawler.getLinks(line,1)
                if links:
                    batch_links.append(links[0])
                else:
                    print('在'+str(index+memory)+'处结束了')
                    if os.path.exists('links/0-'+str(index+memory-len(batch_links)-1)+'_Links.txt'):
                        os.rename('links/0-'+str(index+memory-len(batch_links)-1)+'_Links.txt', 'links/0-'+str(index+memory-1)+'_Links.txt')
                    with open('links/0-'+str(index+memory-1)+'_Links.txt', mode='a', encoding='utf-8') as f:
                        for link in batch_links:
                            f.write("http://www.qichacha.com"+link)
                            f.write('\n')
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
    cookies = ['UM_distinctid=15e564377521e5-019a6849687258-e313761-100200-15e564377541b6; _uab_collina=150468582831443588117478; zg_did=%7B%22did%22%3A%20%2215e5643781640a-0fe292f5fcc46-e313761-100200-15e564378179fa%22%7D; PHPSESSID=s94smovisc8otuk3clajafrpe7; hasShow=1; _umdata=0712F33290AB8A6D314F85E60E62F2BF87D062C800AC554CDD629E4FF8CDC0944F26A250F37ADFFCCD43AD3E795C914CD760D46DA1E3373DE4B870FA68B24E85; CNZZDATA1254842228=2000071625-1504680875-https%253A%252F%252Fwww.baidu.com%252F%7C1516946618; acw_sc__=5a6ac7db93f091ee3edd344ff75f25346fc3138d; acw_tc=AQAAACrOSQhZggUAns54amNV1jR8atLY; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516942716499%2C%22updated%22%3A%201516947682012%2C%22info%22%3A%201516538321075%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22bf3d057349688cafdde40c649ba3bf2f%22%7D',
               ]
    cookie_index = random.randint(0,len(cookies)-1)
    if len(sys.argv)<2:
        next = int(input('请输入起始索引：'))
    else:
        next = int(sys.argv[1])
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

    '''print('Parent process %s.' % os.getpid())
    p = Pool(4)
    p.apply_async(long_time_task, args=(2526,2701,cookies[0]))
    p.apply_async(long_time_task, args=(2963,3001,cookies[1]))
    p.apply_async(long_time_task, args=(3017,3501,cookies[2]))
    p.apply_async(long_time_task, args=(3517,3601,cookies[3]))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')'''