from flask import Flask
from flask import request as req
from flask import render_template as render
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
import visualData as vd

# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

from pyecharts import options as opts
from pyecharts.charts import Pie,Bar,Map,Tab

web = Flask(__name__)

@web.route("/")
def index():
    print('hello')
    hint = "请选择一到两个职位查看可视化的数据"
    job_items = ['区块链','大数据','人工智能','物联网','云计算']
    chartCode = []
    chartCode1 = []
    name_list = []
    for j in job_items:
        data = vd.splitProvince(j)
        m1 = Markup(vd.map_chart(data['number'].items(),
                     '职位数量统计',
                '各省'+j+'职位数量统计').render_embed())
        
       # name_list.append(j+'-岗位数')
        salary = data['salary'].items()
        m2 = Markup(vd.map_chart(salary,'最低薪资平均水平统计','各省'+j+'最低薪资平均水平统计').render_embed())
        chartCode.append([m1,m2])
       # name_list.append(j+'-薪资水平')
        
    return render('index.html',
              #number_tab=Markup(vd.tab_charts(chartCode,job_items).render_embed())
               name_list=job_items,
               chart = chartCode)

@web.route("/visual",methods=['GET','POST'])
def visual():
    if req.method == 'POST':
        try:
            result = dict(req.form)
            key = list(result.keys())
            length = len(key)
            if length ==2 :
                k1 = result[key[0]][0]
                k2 = result[key[1]][0]

                # 为了方便设计图表样式，还是不用循环来简化语句了
                jb1 = vd.countNum(k1,'jobName')
                jb2 = vd.countNum(k2,'jobName')
                
                wordCloud1 = vd.wordCloud_chart(jb1,k1+'\n的岗位描述词','岗位描述词数量').render_embed()
                wordCloud2 = vd.wordCloud_chart(jb2,k2+'\n的岗位描述词','岗位描述词数量').render_embed()
                
                edu1 = vd.countNum(k1,'education')
                edu2 = vd.countNum(k2,'education')

                pie1 = vd.pie_chart(edu1,k1+'\n学历要求统计','学历要求统计',width=720,height=400).render_embed()
                pie2 = vd.pie_chart(edu2,k2+'\n学历要求统计','学历要求统计',width=720,height=400).render_embed()

                sa1 = vd.divid_salary(vd.countNum(k1,'salary'))
                sa2 = vd.divid_salary(vd.countNum(k2,'salary'))

                sa1_bar = vd.bar_chart(sa1,k1+'\n最低薪资水平统计','最低薪资水平统计',width=720,height=400).render_embed()
                sa2_bar = vd.bar_chart(sa2,k2+'\n最低薪资水平统计','最低薪资水平统计',width=720,height=400).render_embed()

                ex1 = vd.countNum(k1,'experience')
                ex2 = vd.countNum(k2,'experience')


                ex1_bar = vd.bar_chart(ex1,k1+'\n工作经验统计','工作经验统计',width=720,height=400).render_embed()
                ex2_bar = vd.bar_chart(ex2,k2+'\n工作经验统计','工作经验统计',width=720,height=400).render_embed()
                c1=c2='col-md-6'
            elif length ==1:
                k1 = result[key[0]][0]
                jb1 = vd.countNum(k1,'jobName')
                wordCloud1 = vd.wordCloud_chart(jb1,k1+'\n的岗位描述词','岗位描述词数量').render_embed()
                
                
                edu1 = vd.countNum(k1,'education')
                pie1 = vd.pie_chart(edu1,k1+'\n学历要求统计','学历要求统计').render_embed()
                
                sa1 = vd.divid_salary(vd.countNum(k1,'salary'))
                sa1_bar = vd.bar_chart(sa1,k1+'\n最低薪资水平统计','最低薪资水平统计').render_embed()
                
                ex1 = vd.countNum(k1,'experience')
                ex1_bar = vd.bar_chart(ex1,k1+'\n工作经验统计','工作经验统计').render_embed()

                wordCloud2 = ex2_bar = sa2_bar = pie2 = ''
                c1 = 'col-md-12'
                c2 = ''
            return render('visual.html',
                      wordCloud1 = Markup(wordCloud1),
                      wordCloud2 = Markup(wordCloud2),
                      pie1 = Markup(pie1),
                      pie2 = Markup(pie2),
                      sa1_bar = Markup(sa1_bar),
                      sa2_bar = Markup(sa2_bar),
                      ex1_bar = Markup(ex1_bar),
                      ex2_bar = Markup(ex2_bar),
                      c1=c1,
                      c2=c2)
        # 说明用户未做任何选择！
        except UnboundLocalError:
            hint = "请选择一或两个工作岗位进行提交！"
            return render('nothing.html',hint=hint)
    elif req.method == 'GET':
        hint = "请使用post方法（提交下面的表单）向/visual发起请求哦"
        return render('nothing.html')

if __name__ == '__main__':
    web.run(debug=True)
    