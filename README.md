### 技术实现
- flask搭建web
- bootstrap排版布局
- pythonanywhere部署项目
- pyecharts可视化数据图表
- boss直聘的全国招聘数据
- requests+beautiful+IP代理池 爬取数据的模块组合
### 项目部署
http://mengzhilang.pythonanywhere.com/ （免费的服务器，如果无人工操作可能要在2020/04/05停止服务）
### 项目描述
爬取boss直聘的全国关于大数据、区块链、物联网、人工智能、云计算的招聘信息，
有全国各个地级市的最低薪资平均水平与岗位数量的地图、岗位描述词的词云、学历要求的饼状图、工作经验的条形图。
从宏观上，为有意愿从事这五个互联网职业的职场小白择业提供可视化的参考。

### 文件目录描述

- main.py 为主程序文件，负责数据流传输、网页路由跳转。
- visualData.py 为模块文件，负责统计与绘图。
- static templates 则是flask常见的放css和js、html网页模板的文件夹了，templates还放了pyecharts规定的一些模块文件，static放了bootstrap的模块文件
- json 专门放已经从boss直聘爬取了全国293地级市、4个直辖市的招聘数据所生成的json文件，但由于网络与程序进程的问题，只生成了922个文件，不过热门城市的数据都已经爬取成功了且boss直聘还没有西藏、台湾、香港、澳门、南沙群岛的数据，所以所采集的数据集还是具有代表性的
```
│  Flask_job.zip
│  Flask_job2.zip
│  Flask_pyechart_job3.zip
│  LICENSE
│  main.py
│  visualData.py
│
├─demo_debug
│  │  demo_code.ipynb
│  │  spider_jobData.ipynb
│  │
│  ├─.ipynb_checkpoints
│  │      demo_code-checkpoint.ipynb
│  │
│  └─__pycache__
│          visualData.cpython-37.pyc
│
├─json
├─static
│  │  background.jpg
│  │  canvas.css
│  │  checkbox.js
│  │  index.css
│  │  jquery.js
│  │  jquery.min.js
│  │  jquery_bg.min.js
│  │
│  ├─.ipynb_checkpoints
│  └─bootstrap
│      ├─css
│      │      bootstrap-theme.css
│      │      bootstrap-theme.css.map
│      │      bootstrap-theme.min.css
│      │      bootstrap-theme.min.css.map
│      │      bootstrap.css
│      │      bootstrap.css.map
│      │      bootstrap.min.css
│      │      bootstrap.min.css.map
│      │
│      ├─fonts
│      │      glyphicons-halflings-regular.eot
│      │      glyphicons-halflings-regular.svg
│      │      glyphicons-halflings-regular.ttf
│      │      glyphicons-halflings-regular.woff
│      │      glyphicons-halflings-regular.woff2
│      │
│      └─js
│              bootstrap.js
│              bootstrap.min.js
│              npm.js
│
└─templates
    │  components.html
    │  index.html
    │  macro
    │  map.html
    │  nb_components.html
    │  nb_jupyter_globe.html
    │  nb_jupyter_lab.html
    │  nb_jupyter_lab_tab.html
    │  nb_jupyter_notebook.html
    │  nb_jupyter_notebook_tab.html
    │  nb_nteract.html
    │  nothing.html
    │  simple_chart.html
    │  simple_globe.html
    │  simple_page.html
    │  simple_tab.html
    │  visual.html
    │
    ├─.ipynb_checkpoints
    └─other
            base.html
            charts.html
            entry.html
            map.html
            results.html
            viewlog.html
```
