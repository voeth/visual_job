#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests as r
from bs4 import BeautifulSoup as bs
# 用于伪造headers，访问者
from faker import Faker


# In[142]:


agent = Faker('zh-CN').user_agent()
def get_cityCode(province='',city=''):
    city_json = 'https://www.zhipin.com/wapi/zpCommon/data/city.json'
    result = r.get(city_json,
                headers={'User-Agent':agent}).json()
    if (result['message'] == 'Success'):
        cityList = result['zpData']['cityList']
        for p in cityList:
            if p['name'] == province:
                sub = p['subLevelModelList']
                flag = 1
                for c in sub:
                    if city == c['name']:
                        return p['code'],c['code']
                return p['code']
        else:
            print('找不到对象')
            return None
    else:
        print('调用boss直聘的获取地区编码的api有问题！',city)


# In[146]:


place = get_cityCode('广东',)
print(place)


# In[161]:


city = get_cityCode('广东','广州')[1]
# 数据上限399条
def get_job(job,city):
    job_json = 'https://www.zhipin.com/mobile/jobs.json'
    params = {
        'query':job,
        'page':1,
        'city':city
    }
    job_data = []
    while 1:
        response = r.get(job_json,
              params=params,
              headers={'User-Agent':agent}).json()
        if response['html']:
            params['page'] +=1
            html = bs(response['html'],'html.parser').find_all(class_='item')
            for h in html:
            # item字典一定要写在循环里面且每遍历完一个职位条目就重新清空字典、保存在job列表当中
            # 否则会重复将最后的值，反复追加到job列表，可见变量名只是个字典的映射。
                item = {}
                item['salary'] = h.find('span',"salary").string
                item['company'] = h.find('div','name').string
                msg = h.find('div','msg').find_all('em')
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


# In[68]:


def count_num(data,key='education'):
    edu = {}
    length = len(data)
    for j in range(length):
        k=data[j][key]
        edu[k] = edu.get(k,0)+1
    return sorted(edu.items(),
                  key=lambda x : x[1],
                  reverse=True)


# In[185]:


from pyecharts import options as opts
from pyecharts.charts import Pie,Bar,Map,Tab
from pyecharts.faker import Faker


# In[53]:


def pie_chart(data,title,seriers_name):
    try:
        c = (
            Pie()
            .add(seriers_name,data)
            .set_global_opts(title_opts=opts.TitleOpts(title=title))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        return c
    except ValueError:
        print("请输入正确的数据格式！比如：[('本科', 290), ('大专', 88), ('学历不限', 16), ('高中', 5), ('中专/中技', 1)]")
job = get_job('产品经理',get_cityCode('广东','佛山'))
edu_data = count_num(job,'education')
pie_chart(edu_data,'产品经理的学历要求','该学历要求的数量统计').render_notebook()


# In[109]:


def bar_chart(ex_data,title='',seriers_name='',color='red'):
    xaxis = list(dict(ex_data).keys())
    yaxis = list(dict(ex_data).values())
    c = (
        Bar()
        .add_xaxis(xaxis)
        .add_yaxis(seriers_name,yaxis,color=color)
  #      .set_series_opts(label_opts=opts.LabelOpts(color='blue'))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            datazoom_opts=opts.DataZoomOpts()
        )
    )
    return c


# In[111]:


def divid_salary(data):
    # 依据个人所得税税率表来将salary数据分组，否则太多太杂了。
    # 以月薪、千元为单位
    if isinstance(data,dict):
        sk = {'<3k':0,'3-12k':0,'12-25k':0,'25-35k':0,'35-55k':0,'55k-80k':0,'>80k':0}
        for s in data:
            # 由于我们的产品目标是为职场小白提供择业意见，小白往往只能获得最低工资，所以我们仅选取了最低工资，方便将每个工资范围进行分组
            sl = s.split('-')
            d = data[s]
            if sl[1][-1] == 'K':
                key = int(sl[0])
                if key <=3:
                    sk['<3k'] += d
                elif key > 3 and key <= 12:
                    sk['3-12k'] += d
                elif key > 12 and key <= 25:
                    sk['12-25k'] += d
                elif key > 25 and key <= 35:
                    sk['25-35k'] += d
                elif key > 35 and key <= 55:
                    sk['35-55k'] += d
                elif key > 55 and key <= 80:
                    sk['55-80k'] += d
                elif key > 80:
                    sk['>80k'] += d
        result = sorted(sk.items(),key=lambda x:x[1],reverse=True)
        return result
    else:
        print('请输入字典类型的数据。')
sa = divid_salary(dict(count_num(job,'salary')))
bar_chart(sa,'产品经理薪资水平统计','该薪资水平的数量统计',color='red').render_notebook()


# In[112]:


exnum = count_num(job,'experience')
bar_chart(exnum,color='black').render_notebook()


# In[184]:



# 要单独将地图可视化放到另一个页面才行。
def get_mapData(jobName):
    city_json = 'https://www.zhipin.com/wapi/zpCommon/data/city.json'
    adv = r.get(city_json,
                    headers={'User-Agent':agent}).json()['zpData']['cityList']

    # 创建一个市级行政区域与省级行政区的映射，方便后面统计各省的职位数量
    pt = {}
    for ad in adv:
        for a in ad['subLevelModelList']:
            pt[a['name']] = ad['name']

    # 先统计每个城市的职位数量，再统计省级行政区的职位数量
    pycity = count_num(get_job(jobName,100010000),'city')
    map_data = {}
    for p in pycity:
        key = pt[p[0]]
        map_data[key]= map_data.get(key,0)+p[1]
    return map_data.items()

def map_chart(data,series_name,title):
    mapData = list(data)
    c = (
        Map()
        .add(series_name,mapData)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            visualmap_opts=opts.VisualMapOpts(max_= mapData[0][1])
        )
    )
    return c

map_chart(get_mapData('计算机老师'),'该岗位的需求数量：','计算机教师岗位需求').render()


# In[192]:


salary = dict(count_num(job,'salary'))
tab = Tab()
tab.add(bar_chart(divid_salary(salary),'产品经理薪资水平统计','该薪资水平的数量统计',color='red'),'产品经理薪资水平统计')
tab.add(bar_chart(count_num(job,'experience'),color='black'),'产品经理工作经验统计')
tab.add(pie_chart(count_num(job,'education'),'产品经理的学历要求','该学历要求的数量统计'),'产品经理学历要求统计')
tab.render()


# In[ ]:



