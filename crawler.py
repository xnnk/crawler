import re
from urllib import request
from io import BytesIO
import gzip

class Spider():

    # 目标网址
    url = 'https://www.douyu.com/'

    # 初步匹配(标签内全选且非贪婪)
    initial_regex = '<div class="DyListCover-content">([\s\S]*?)</h2></div>'

    # 主播名字匹配
    name_regex = '<div class="DyListCover-userName is-template">([\s\S]*?)</div>'

    # 主播直播间信息匹配
    live_title_regex = '<h3 class="DyListCover-intro" title="(.*?)">'

    # 主播热度信息匹配
    heat_regex = '<span class="DyListCover-hot is-template"><svg>.*?</svg>(.*?)</span>'

    # 获取内容方法 
    def __get_content(self, game): 
        result = request.urlopen(Spider.url+game)
        # bytes转义
        htmls = result.read()
        # gzip解码
        buff = BytesIO(htmls)
        f = gzip.GzipFile(fileobj=buff)
        htmls = f.read().decode('utf-8')
        return htmls

    # 提取并精炼数据
    def __analysis(self, htmls): 
        pattern = re.compile(Spider.initial_regex)
        initial_htmls = pattern.findall(htmls)

        # 列表遍历并提取信息
        info_list = []
        for html in initial_htmls: 
            name = re.findall(Spider.name_regex, html)
            live_title = re.findall(Spider.live_title_regex, html)
            heat = re.findall(Spider.heat_regex, html)

            # 封装成三元组并存入列表中
            dist = (name[0], live_title[0], heat[0])
            info_list.append(dist)
        return info_list

    def __sort(self, list): 
        # 根据热度排序(x[2][:-1]定位到第三索引并去掉末尾的"万")
        sorted_list = sorted(list, key=lambda x: float(x[2][:-1]), reverse=True)
        return sorted_list

    def connect(self): 
        url_map = {
                    '英雄联盟':'g_LOL','无畏契约':'g_VALORANT','穿越火线':'g_CF','和平精英':'g_hpjy','刀塔2':'g_DOTA2',
                    '王者荣耀':'g_wzry','英雄联盟手游':'g_LOLM','金铲铲之战':'g_JGAME','生死狙击2':'g_ssjjtwo',
                    '暗区突围':'g_aqtw','地下城与勇士':'g_DNF','原神':'g_yuanshen','APEX':'g_APEX','逃离塔科夫':'g_EFT',
                    '主机游戏':'g_TVgame','QQ飞车':'g_qqfcsy','炉石传说':'g_How'
                  }
        name = input('查找相关游戏的主播信息（可选 英雄联盟，无畏契约，穿越火线，和平精英，刀塔2，王者荣耀，英雄联盟手游，金铲铲之战，生死狙击2，暗区突围，地下城与勇士，原神，APEX，逃离塔科夫，主机游戏，QQ飞车，炉石传说）')
        game_name = url_map.get(name)
        htmls = self.__get_content(game_name)
        list = self.__analysis(htmls)
        sorted_list = self.__sort(list)
        for i in sorted_list: 
            print(i)



# 运行
spider = Spider()
spider.connect()
