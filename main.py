# -*- coding: utf-8 -*-
import time
import logging
import sys
import re
import urllib2
import random

from bs4 import BeautifulSoup as Bs
from collections import Counter
from https import Http
from parse import Parse
from setting import headers
from setting import cookies
from setting import UA

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s Process%(process)d:%(thread)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='diary.log',
                    filemode='a')


def getInfo(url, para):
    """
    获取信息
    """
    generalHttp = Http()
    htmlCode = generalHttp.post(url, para=para, headers=headers, cookies=cookies)
    generalParse = Parse(htmlCode)
    pageCount = generalParse.parsePage()
    info = []
    for i in range(1, pageCount + 1):
        print('第%s页' % i)
        para['pn'] = str(i)
        htmlCode = generalHttp.post(url, para=para, headers=headers, cookies=cookies)
        generalParse = Parse(htmlCode)
        info = info + getInfoDetail(generalParse)
        time.sleep(5)
        if i == 10:
            return info
    return info


def getInfoDetail(generalParse):
    """
    信息解析
    """
    info = generalParse.parseInfo()
    return info


def processInfo(info, para):
    """
    信息存储
    """
    logging.error('Process start')
    try:
        #title = '公司名称\t公司类型\t融资阶段\t公司规模\t公司所在地\t职位类型\t学历要求\t福利\t薪资\t工作经验\n'
        #file = codecs.open('%s职位.xls' % para['city'], 'w', 'utf-8')
        #file.write(title)
        for p in info:
            #line = str(p['companyName']) + '\t' + str(p['companyType']) + '\t' + str(p['companyStage']) + '\t' + \
                   #str(p['companySize']) + '\t' + str(p['companyDistrict']) + '\t' + str(p['positionType']) + '\t' + \
                   #str(p['positionEducation']) + '\t' + str(p['positionAdvantage']) + '\t' + \
                   #str(p['positionSalary']) + '\t' + str(p['positionWorkYear']) + '\n'
            #file.write(line)
            content = get_content(p['positionId'])
            result = get_result(content)
            skil_list = search_skill(result)
            print skil_list
            count_dict = count_skill(skil_list)
            print count_dict
            time.sleep(60)
        #file.close()
        return True
    except Exception as e:
        print(e)
        pass


def get_content(company_id):
    fin_url = r'http://www.lagou.com/jobs/%s.html' % company_id
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'www.lagou.com',
        'Connection': 'keep-alive',
        'Origin': 'http://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_Python?px=default&city=%E5%8C%97%E4%BA%AC',
        'Cookie': 'WEBTJ-ID=20180717160550-164a7462ac9773-0722e4e40085ad-f373567-1327104-164a7462aca861; _ga=GA1.2.1016908786.1531814751; user_trace_token=20180717160552-39620249-8998-11e8-9e0d-5254005c3644; LGUID=20180717160552-39620649-8998-11e8-9e0d-5254005c3644; X_HTTP_TOKEN=a6ad9b85992858abe43e93039bf0e27e; _putrc=532B47117DEBEDB9; JSESSIONID=ABAAABAAADEAAFI5DD246CC43A9A130D33552AAE4FB6A5D; login=true; unick=%E5%88%98%E4%BC%9F; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=5; index_location_city=%E5%8C%97%E4%BA%AC; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531814751,1532755383; _gat=1; LGSID=20180728132303-4d2b2cd7-9226-11e8-a067-5254005c3644; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26rsv_spt%3D1%26rsv_iqid%3D0xeee42948000166d6%26issp%3D1%26f%3D8%26rsv_bp%3D1%26rsv_idx%3D2%26ie%3Dutf-8%26rqlang%3Dcn%26tn%3Dbaiduhome_pg%26rsv_enter%3D0%26oq%3D%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E7%2525BD%252591%2525E5%25258F%25258D%2525E7%252588%2525AC%2525E8%252599%2525AB%26rsv_t%3Dfa82P%252Beva%252BrkoPkGZDhBTOKshix66GoTAMxPQ%252FE3obpx9TI7isQQ0pYZaiErwvJcmB1C%26rsv_pq%3D84cbe4a70002bbc7%26inputT%3D1243%26rsv_sug3%3D37%26rsv_sug1%3D26%26rsv_sug7%3D100%26rsv_sug2%3D0%26rsv_sug4%3D1243%26rsv_sug%3D1; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; _gid=GA1.2.1954639909.1532755383; LG_LOGIN_USER_ID=fd4024ca28bd0e210404ebe1735f0b7314e22b1bf159e045; gate_login_token=d47ca53f2120aa58b72dc1818b3d9df041f77870b5d9f04f; SEARCH_ID=f284b2cded8349e5b9d68532c2bcee68; TG-TRACK-CODE=search_code; LGRID=20180728132424-7d5b5249-9226-11e8-a067-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1532755464',
    }
    req = urllib2.Request(fin_url, headers=headers)
    page = urllib2.urlopen(req).read()
    content = page.decode('utf-8')
    return content

#获取职位需求（通过re来去除html标记），可以将职位详情单独存储
def get_result(content):
    soup = Bs(content, 'lxml')
    job_description = soup.select('dd[class="job_bt"]')
    job_description = str(job_description[0])
    rule = re.compile(r'<[^>]+>')
    result = rule.sub('', job_description)
    return result

#过滤关键词
def search_skill(result):
    rule = re.compile(r'[a-zA-z]+')
    skil_list = rule.findall(result)
    return skil_list

# 对出现的关键词计数，并排序，选取Top80的关键词作为数据的样本
def count_skill(skill_list):
    for i in range(len(skill_list)):
        skill_list[i] = skill_list[i].lower()
    count_dict = Counter(skill_list).most_common(80)
    return count_dict


def main(url, para):
    """
    主函数逻辑
    """
    logging.error('Main start')
    if url:
        info = getInfo(url, para)  # 获取信息
        flag = processInfo(info, para)  # 信息储存
        return flag
    else:
        return None


reload(sys)
sys.setdefaultencoding('utf8')
if __name__ == '__main__':
    kdList = [u'python']
    cityList = [u'北京']
    url = 'https://www.lagou.com/jobs/positionAjax.json'
    for city in cityList:
        print('爬取%s'% city)
        para = {'first': 'true', 'pn': '1', 'kd': kdList[0], 'city': city}
        flag = main(url, para)
        if flag:
            print('%s爬取成功' % city)
        else:
            print('%s爬取失败' % city)
