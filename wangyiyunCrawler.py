import re
from urllib import request
import string
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

class Spider():

    # 目标网址
    url = 'https://music.163.com/m/artist/album?id='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    # 歌手专辑总页面基址
    album_url = 'https://music.163.com/m/artist'

    # 歌手单专辑页面基址
    song_album_url = 'https://music.163.com/m'

    # 页面offset
    offset = 0

    singerId = ''

    singer_name = ''

    album_urls = []

    # 二元组结构集合 [(专辑名, 歌曲名)]
    result_dist_list = []

    # 歌手名字匹配
    singer_regex = ''

    # 歌手专辑url匹配
    album_url_regex = '<a href="(.*?)" class="msk"></a>'

    # 歌手专辑名匹配
    album_name_regex = '<div class="tit">\n<h2 class="f-ff2">(.*?)</h2>\n</div>'

    # 歌手单专辑歌曲标题匹配
    song_title_regex1 = '<ul class="f-hide"><li>(.*?)</li></ul>'

    song_title_regex2 = '">(.*?)</a>'


    # 获取内容方法 
    def __get_content(self, url): 
        url = quote(url, safe=string.printable)
        result = request.Request(url, headers=Spider.headers)
        response = urlopen(result)
        response = response.read()
        response = response.decode('utf-8')
        # print(response)
        return response

    # 提取歌手名字
    def __analysis_name(self, htmls): 
        pattern = re.compile(Spider.singer_regex)
        name = pattern.findall(htmls)

        return name[0]

    # 获取本页的所有专辑
    def __getPageAlbumURL(self, htmls): 
        
        # 提取本页的专辑url
        pattern = re.compile(Spider.album_url_regex)
        album_urls = pattern.findall(htmls)
        if len(album_urls) == 0 : 
            return False
        for url in album_urls: 
            Spider.album_urls.append(url)
        return True

            
    # 获取所有专辑url
    def __getAllAlbumURL(self): 
        # https://music.163.com/m
        album_url = Spider.album_url + '/album?id=' + Spider.singerId + '&limit=12&offset='
        while True: 
            cur_album_url = album_url + str(Spider.offset)
            Spider.offset = Spider.offset + 12
            htmlq = self.__get_content(cur_album_url)
            # 获取每页的专辑url
            flag = self.__getPageAlbumURL(htmlq)
            if not flag: 
                break

    # 获取单个专辑里的歌曲和歌手
    def __getOneAlbumSongs(self, album_url): 
        cur_album_url = Spider.song_album_url + album_url
        htmls = self.__get_content(cur_album_url)

        # 提取专辑名
        album_name_pattern = re.compile(Spider.album_name_regex)
        album_names = album_name_pattern.findall(htmls)
        if len(album_names) == 0: 
            return
        album_name = album_names[0]

        # 提取歌曲标题
        song_title_pattern1 = re.compile(Spider.song_title_regex1)
        song_titles1 = song_title_pattern1.findall(htmls)
        song_title_pattern2 = re.compile(Spider.song_title_regex2)
        song_titles = song_title_pattern2.findall(song_titles1[0])

        # 创建二元组元素
        dist_list = []
        for i in range(len(song_titles)): 
            dist = (album_name, song_titles[i])
            dist_list.append(dist)
        Spider.result_dist_list.append(dist_list)
        # print(dist_list)
        # print("\n------------------------------------------------------------------\n")

    # 获取所有专辑里的歌曲和歌手
    def __getAllAlbumSongs(self): 
        ablums_urls = Spider.album_urls
        for url in ablums_urls: 
            self.__getOneAlbumSongs(url)


    def connect(self): 
        Spider.singerId = input('歌手id:')
        Spider.url = Spider.url + Spider.singerId
        
        # 歌手名字匹配
        Spider.singer_regex = '<h2 id="artist-name" data-rid='+Spider.singerId+' class="sname f-thide sname-max" title="(.+?)">'

        # 获取网易云原始内容
        htmls = self.__get_content(Spider.url)

        # 获取歌手名字
        Spider.singer_name = self.__analysis_name(htmls)

        # 获取本歌手的所有专辑url
        self.__getAllAlbumURL()

        # 获取所有专辑的所有歌曲
        self.__getAllAlbumSongs()

        # 一次性展示所有内容
        print(Spider.result_dist_list)

# 运行
spider = Spider()
spider.connect()
