import requests as r
from requests import exceptions as req_bug
from bs4 import BeautifulSoup as bs
import random
import glob
import json

# 用于伪造headers，访问者
from faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Pie,Bar,Map,Tab,Grid,WordCloud


agent = Faker(locale='zh-CN').user_agent()
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

# 数据上限399条
def get_job(job,city):
    proxies = [{'http':'http://47.107.175.190:8000'},
          {'http':'http://163.204.242.64:9999'},
          {'http':'http://47.112.214.45:8000'},
        {'http':'http://163.204.242.181:9999'},
        {'http':'http://163.204.241.214:9999'}]
    
    job_json = 'https://www.zhipin.com/mobile/jobs.json'
    params = {
        'query':job,
        'page':1,
        'city':city
    }
    job_data = []
    while 1:
        pro = random.choice(proxies)
        response = r.get(job_json,
              params=params,
              headers={'User-Agent':agent},
            proxies=pro).json()
        
        try:
            
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
            elif response['html'] == '' and params['page']==1:
                print('用户输入的关键词有误，找不到对象！')
                return None
                break
            else:
                break
        # 返回的json数据结果没有html键，说明ip已被封
        except KeyError:
            print(response)
            break
        # 连接代理服务出现异常时，就把那个代理ip从列表中删除并继续用另一个代理ip
        except (ConnectTimeout,ProxyError,ReadTimeout):
            proxies.remove(pro)
            continue
    return job_data


# 数据统计分析
# fkey [大数据 人工智能 区块链 物联网 云计算 ]
# kw ['salary' 'education' 'jobname' 'experience']
def countNum(fkey,kw):
    try:
        file = glob.glob('json/'+fkey+'_*_*.json')
        edu_num = {kw:{}}
        for ff in file:
            with open(ff) as f:
                content = json.loads(f.read())
                for j in content[kw]:
                    edu_num[kw][j] = edu_num[kw].get(j,0)+1
        return sorted(edu_num[kw].items(),key= lambda x:x[1],reverse=True)
    except KeyError:
        print("请输入正确的关键词\n fkey [大数据 人工智能 区块链 物联网 云计算 ]\n 请输入正确的关键词\n fkey [大数据 人工智能 区块链 物联网 云计算 ]\n")

def divid_salary(Data):
    # 依据个人所得税税率表来将salary数据分组，否则太多太杂了。
    # 以月薪、千元为单位
    try:
        data = dict(Data)
        sk = {'<3k':0,'3-12k':0,'12-25k':0,'25-35k':0,'35-55k':0,'55-80k':0,'>80k':0}
        for s in data:
            # 由于我们的产品目标是为职场小白提供择业意见，小白往往只能获得最低工资，所以我们仅选取了最低工资，方便将每个工资范围进行分组
            sl = s.split('-')
            if sl[1][-1] == 'K':
                key = int(sl[0])
                if key <=3:
                    sk['<3k'] += data[s]
                elif key > 3 and key <= 12:
                    sk['3-12k'] += data[s]
                elif key > 12 and key <= 25:
                    sk['12-25k'] += data[s]
                elif key > 25 and key <= 35:
                    sk['25-35k'] += data[s]
                elif key > 35 and key <= 55:
                    sk['35-55k'] += data[s]
                elif key > 55 and key <= 80:
                    sk['55-80k'] += data[s]
                elif key > 80:
                    sk['>80k'] +=data[s]
        result = sorted(sk.items(),key=lambda x:x[1],reverse=True)
        return result
    
    except TypeError:
        print("请输入正确的数据格式！比如：[('本科', 290), ('大专', 88), ('学历不限', 16), ('高中', 5), ('中专/中技', 1)]")

# 分省统计方便地图可视化        
def splitProvince(fkey):
    flist = glob.glob('json/'+fkey+'_*_*.json')
    
    sp = {'number':{},'salary':{}}
    if len(flist):
        for fl in flist:
            j,p,c = fl.split('_')
            with open(fl) as f:
                data = json.loads(f.read())
                sp['number'][p] = len(data['salary'])
                count = 0
                for d in data['salary']:
                    s = int(d.split('-')[0])*1000
                    count +=int(s/sp['number'][p])
                sp['salary'][p] = count
        return {'number':sp['number'],'salary':sp['salary']}
    else:
        print("请输入正确的关键词\n fkey [大数据 人工智能 区块链 物联网 云计算 ]\n 请输入正确的关键词\n fkey [大数据 人工智能 区块链 物联网 云计算 ]\n")


# 渲染图表的函数代码，建议图表都保持9:5的长宽比，保持美感
def pie_chart(data,title,seriers_name,width=900,height=500):
    try:
        w = str(width)+'px'
        h = str(height)+'px'
        c = (
            Pie(init_opts=opts.InitOpts(width=w,height=h))
            .add(seriers_name,data)
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
               # 加了datzoom后就加载不出图片了map也是如此 datazoom_opts=opts.DataZoomOpts(),
                       toolbox_opts=opts.ToolboxOpts(is_show=True,orient='vertical'))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        return c
    except ValueError:
        print("请输入正确的数据格式！比如：[('本科', 290), ('大专', 88), ('学历不限', 16), ('高中', 5), ('中专/中技', 1)]")


def bar_chart(ex_data,title='',seriers_name='',color='red',width=900,height=500):
    xaxis = list(dict(ex_data).keys())
    yaxis = list(dict(ex_data).values())
    w = str(width)+'px'
    h = str(height)+'px'
    c = (
        Bar(init_opts=opts.InitOpts(width=w,height=h))
        .add_xaxis(xaxis)
        .add_yaxis(seriers_name,yaxis,color=color)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            datazoom_opts=opts.DataZoomOpts(),
            toolbox_opts=opts.ToolboxOpts(is_show=True,orient='vertical')
        )
    )
    return c

def map_chart(data,series_name,title,width=900,height=500):
    mapData = list(data)
    w = str(width)+'px'
    h = str(height)+'px'
    c = (
        Map(init_opts=opts.InitOpts(width=w,height=h))
        .add(series_name,mapData)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            visualmap_opts=opts.VisualMapOpts(max_= mapData[0][1]),
            toolbox_opts=opts.ToolboxOpts(is_show=True,orient='vertical')
        )
    )  
    return c

def wordCloud_chart(data,title,series='',width=900,height=500):
    w = str(width)+'px'
    h = str(height)+'px'
    c = (
        WordCloud(init_opts=opts.InitOpts(width=w,height=h))
        .add(series,data,word_size_range=[20,100],shape='triangle-forward')
        .set_global_opts(title_opts=opts.TitleOpts(title=title))
    )
    return c

def tab_charts(chart_list,name_list):
    clen = len(chart_list)
    nlen = len(name_list)
    if clen == nlen:
        tab = Tab()
        for c in range(clen):
            tab.add(chart_list[c],name_list[c])   
        return tab
    else:
        print('请确保图表代码与图表名称一一对应')
    
