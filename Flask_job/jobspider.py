import requests as r
from bs4 import BeautifulSoup as bs
# 用于伪造headers，访问者
from faker import Faker

agent = Faker('zh-CN').user_agent()


def get_cityCode(province='', city=''):
    city_json = 'https://www.zhipin.com/wapi/zpCommon/data/city.json'
    result = r.get(city_json,
                   headers={'User-Agent': agent}).json()
    if (province != '' and city != '' and result['message'] == 'Success'):
        cityList = result['zpData']['cityList']
        for p in cityList:
            if p['name'] == province:
                sub = p['subLevelModelList']
                flag = 1
                for c in sub:
                    if city == c['name']:
                        return c['code']
        else:
            print('找不到对象')
            return None
    elif (province == city == ''):
        print('不输入地名则默认为全国')
        return 100010000
    else:
        print('调用boss直聘的获取地区编码的api有问题！', city)


city = get_cityCode('广东', '广州')


def get_job(job, city):
    job_json = 'https://www.zhipin.com/mobile/jobs.json'
    params = {
        'query': job,
        'page': 1,
        'city': city
    }
    job_data = []
    while 1:
        response = r.get(job_json,
                         params=params,
                         headers={'User-Agent': agent}).json()
        if response['html']:
            params['page'] += 1
            html = bs(response['html'], 'html.parser').find_all(class_='item')
            for h in html:
                # item字典一定要写在循环里面且每遍历完一个职位条目就重新清空字典、保存在job列表当中
                # 否则会重复将最后的值，反复追加到job列表，可见变量名只是个字典的映射。
                item = {}
                item['salary'] = h.find('span', "salary").string
                item['company'] = h.find('div', 'name').string
                msg = h.find('div', 'msg').find_all('em')
                for em in range(3):
                    item['city'] = msg[0].string
                    item['experience'] = msg[1].string
                    item['education'] = msg[2].string
                job_data.append(item)
        elif response['resmsg'] != '成功':
            print('调用boss直聘获取工作列表api有问题！或者是网络、服务器有问题')
            continue
        else:
            break
    return job_data


job = get_job('产品经理', city)


def count_num(data, key='education'):
    edu = {}
    length = len(data)
    for j in range(length):
        k = data[j][key]
        edu[k] = edu.get(k, 0) + 1
    return edu


result = count_num(job, 'education')
print(result, job)