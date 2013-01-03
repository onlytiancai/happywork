# Happy Work

做一些提高工作效率的小工具，目前先实现了一个TODO，这里有[演示地址](http://happywork.sinaapp.com/todo/index.html)可以试用。

### TODO FAQ

1. 这个TODO App是做什么的，适合我用吗？
    1. 如果你经常感觉每天很忙，到月底却不知道到底做了些什么，那这个APP就很适合你。
    1. 它可以帮助你记录要做的事情，防止太忙而遗忘掉某些工作。
    1. 它可以让你察看每周都都做了哪些事情，方便你写周总结和月总结。
1. 我的工作内容是保密的，不适合放在外网呀。
    1. 亲，这个程序是开源的，你可以让运维部署到公司内网，见后面的链接。
    1. 如果不方便搭建在公司内网，也可以在SAE搭建一个，所有数据都是你自己管理的。
1. 我的工作项太多了，我想知道哪些是我正在进行的工作？
    1. 在要进行的工作项右侧的【操作】按钮里点【开始执行】，该工作项会变蓝。
1. 我本周的工作项太多了，我能不能给某项工作设置个最后期限？
    1. 在该工作项右侧的【操作】按钮里点击【设置最后期限】就可以，如果到时候还没完成工作，该工作项就会变红。
1. 我如何察看本周或上周完成的工作？
    1. 点右上角的【已完成事项】就看到了，可以察看你每周都做了什么事情，你会很有成就感的。

### 部署到本机 

1: 项目初始化

    make init

2: 本机安装好mysql，修改 ./stuff/webappbox_config.py里的响应配置

3: 安装依赖

    pip install -r ./webappbox/requirements.txt

4: 启动程序

    make start

5: 浏览器里打开http://localhost:8803


### 部署到SAE

如下

1.make init 初始化项目
1. ./webappbox/src/config.py 里的use_SAE = True
1. webappbox/src/webapps/login/config.py里的qq和weibo登陆的appkey等需要配置
1. 然后把webappbox/src目录下的所有文件上传到SAE里就行了
