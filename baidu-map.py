#!/usr/bin/python
#coding=utf-8

from feedback import Feedback
import urllib2
import urllib
import json
import sys
import os.path

AK = '61d9c2b7e886b8f2e5bad831917b1c8d'  # 默认AK
CITY = '北京'
API_URL_BASE = 'http://api.map.baidu.com'
MAP_URL_BASE = 'http://map.baidu.com'


def main(args):
    if os.path.exists('city.txt'):
        CITY = file('city.txt', 'r').read().strip('\r\n \t')

    region = urllib.quote(CITY)
    feeds = Feedback()

    if len(args) == 2:  # 有参数的才进行分析
        if '到' in args[1] or '去' in args[1]:  # 调用导航的API来做操作
            if '到' in args[1]:
                location = args[1].split('到')
            elif '去' in args[1]:
                location = args[1].split('去')

            map_url = '%s/direction?origin=%s&destination=%s&mode=transit&region=%s&output=html&src=alfredapp.baidumap.search' % (
                API_URL_BASE, urllib.quote(
                    location[0]), urllib.quote(location[1]), region)
            feeds.add_item(title=unicode(args[1], 'utf-8'), subtitle=unicode(CITY, 'utf-8'),
                           valid='YES', arg=map_url, icon='icon.png')
        else:
            query = urllib.quote(args[1])

            result = json.load(urllib2.urlopen(
                '%s/place/v2/search?&q=%s&region=%s&output=json&ak=%s' % (API_URL_BASE, query, region, AK)))

            if result['status'] == 0:
                for i in result['results']:
                    name = i.get('name', '搜索不到结果')
                    address = i.get('address', '')
                    uid = i.get('uid', '')

                    map_url = '%s/?newmap=1&s=inf%%26uid%%3D%s%%26wd%%3D%s' % (
                        MAP_URL_BASE, uid, name)

                    feeds.add_item(title=name, subtitle=address,
                                   valid='YES', arg=map_url, icon='icon.png')
            else:
                feeds.add_item(title=u'内容未找到', subtitle=u'输入内容有误',
                               valid='no', arg=MAP_URL_BASE, icon='icon.png')

        print feeds  # 最终输出结果
    return


if __name__ == '__main__':
    main(sys.argv)
