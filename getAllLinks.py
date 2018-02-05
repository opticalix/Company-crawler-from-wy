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

# 对batch和memory的命名比较疑惑, 用于计数的话可以叫count, batch是用于缓冲后再一次性做IO?
def long_time_task(fname, index, endIndex, cookie, batch_size=5):
    print('long_time_task, index=%d, endIndex=%d' % (index, endIndex))
    memory = 0
    crawler = Qichacha_crawler(cookie)
    with open(fname, 'r') as f:
        data = f.readlines()[index:endIndex]
        batch_num = math.ceil(len(data)/batch_size)
        for i in range(batch_num):
            batch_data = data[i*batch_size:(i+1)*batch_size]
            batch_links = []
            # print('batch_data=%s' % batch_data)
            for line in batch_data:
                line = line.replace('\n', '')
                print('before get link, company_name = %s' % line)
                links = crawler.getLinks(line,1)
                try_time = 0
                while not links and try_time<3:
                    try_time+=1
                    links = crawler.getLinks(line,1)
                if links:
                    batch_links.append(links[0])
                else:
                    print('在'+str(index+memory)+'处结束了')
                    save_link(index, memory, batch_links)
                    next = index+memory
                    return next
                memory+=1
                # print(index+memory)
            save_link(index, memory, batch_links)
    return index+memory

# 同样的代码抽成func. 
# 字符串拼接推荐用 '%s%s' % (x1,x2) 的方式
# 另外我觉得所有link都存在一起的风险比较大 可以每1000个分一个txt. 万一中间有几个link出了问题顺序对不上就麻烦了
def save_link(index, memory, batch_links):
    old = str(index+memory-len(batch_links)-1)
    new = str(index+memory-1)
    dir_name = 'links'#可自定义 并需要check exists
    old_file = '%s/0-%s_Links.txt' % (dir_name, old)
    new_file = '%s/0-%s_Links.txt' % (dir_name, new)

    if os.path.exists(old_file):
        os.rename(old_file, new_file)
    with open(new_file, mode='a', encoding='utf-8') as f:
        for link in batch_links:
            f.write("http://www.qichacha.com"+link)
            f.write('\n')


if __name__=='__main__':
    #define vars
    failed_time = 0
    all_cnt = 20
    step = min(10, all_cnt)
    company_list_filename = 'company_name_utf8.txt'#你给我的是gbk格式我这打开乱码 转成utf8了 应该更通用
    cookies = ['UM_distinctid=15e564377521e5-019a6849687258-e313761-100200-15e564377541b6; _uab_collina=150468582831443588117478; zg_did=%7B%22did%22%3A%20%2215e5643781640a-0fe292f5fcc46-e313761-100200-15e564378179fa%22%7D; PHPSESSID=s94smovisc8otuk3clajafrpe7; hasShow=1; _umdata=0712F33290AB8A6D314F85E60E62F2BF87D062C800AC554CDD629E4FF8CDC0944F26A250F37ADFFCCD43AD3E795C914CD760D46DA1E3373DE4B870FA68B24E85; CNZZDATA1254842228=2000071625-1504680875-https%253A%252F%252Fwww.baidu.com%252F%7C1516946618; acw_sc__=5a6ac7db93f091ee3edd344ff75f25346fc3138d; acw_tc=AQAAACrOSQhZggUAns54amNV1jR8atLY; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516942716499%2C%22updated%22%3A%201516947682012%2C%22info%22%3A%201516538321075%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22bf3d057349688cafdde40c649ba3bf2f%22%7D',
               ]#这里不需要多cookie吗?
    cookie_index = random.randint(0,len(cookies)-1)

    if len(sys.argv)<2:
        next = int(input('请输入起始索引：'))
    else:
        next = int(sys.argv[1])

    while next<all_cnt:
        pre = next
        next = long_time_task(company_list_filename, next,next+step,cookies[cookie_index],5)#何时加空格 比如我一般都写成[next < all_cnt][next, next + step, xxx...] 建议遵守大厂的代码格式 一般大厂code review时格式卡的很严..
        print('long_time_task ret = %d' % next)
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