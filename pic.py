import os
import re
import requests
from lxml import etree
from PIL import Image
from time import sleep

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Referer': 'https://t1.chei.com.cn/'
}

# 省份简称
provinces = ['31', '32', '33']
# 31-上海 32-江苏 33-浙江

results = []

# 创建Image文件夹
IMAGE_DIR = "D:/VScode/python/Image"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

with requests.Session() as session:
    for province in provinces:
        url = f'https://yz.chsi.com.cn/sch/search.do?ssdm={province}&yxls=&ylgx=&yjsy=&zhx='
        response = session.get(url, headers=HEADERS)
        if response.status_code == 200:
            html = response.content
            selector = etree.HTML(html)

            # 获取高校列表
            schools = selector.xpath(
                '//*[@class="main-wrapper"]/div[4]/div[2]/div[@class="sch-item"]'
            )

            for school in schools:
                school_url = school.xpath(
                    './div/div[@class="sch-title"]/a/@href')[0]
                school_name = school.xpath(
                    './div/div[@class="sch-title"]/a/text()')[0]
                logo_url = school.xpath('./img/@src')[0]
                print(logo_url)

                # 下载图片
                picture = session.get(logo_url)

                # 将图片的文件名改为学校名称，并添加后缀名
                filename = re.sub(r'\W+', '_', school_name) + '.jpg'

                # 保存图片到Image文件夹中
                with open(os.path.join(IMAGE_DIR, filename), 'wb') as f:
                    f.write(picture.content)

                try:
                    # 使用PIL库检查下载的图片是否正确
                    Image.open(os.path.join(IMAGE_DIR, filename))
                except Exception as e:
                    print(f"Error: {e}")

                # 进入每个高校页面爬取数据
                try:
                    response = session.get(
                        f'https://yz.chsi.com.cn{school_url}', headers=HEADERS)
                    print(f"Processing {school_name}...")
                    if response.status_code == 200:
                        html = response.content
                        selector = etree.HTML(html)

                        # 招生简章链接
                        recruit_notice_url = selector.xpath(
                            '//*[@class="main-wrapper"]/div[4]/div[2]/div[@class="sch-item"]/div[1]/div[3]/a[2]/@href'
                        )
                        recruit_notice_url = recruit_notice_url[
                            0] if recruit_notice_url else ''

                        if recruit_notice_url and province in [
                                '31', '32', '33'
                        ]:
                            results.append({
                                '院校名称':
                                school_name,
                                '调剂方法链接':
                                f'https://yz.chsi.com.cn{school_url}',
                                '招生简章链接':
                                f'https://yz.chsi.com.cn{recruit_notice_url}'
                            })

                            sleep(3)

                except Exception as e:
                    print(f"Error while processing {school_name}: {e}")

                sleep(2)

SLEEP_TIME = 2
for result in results:
    print(result)
    sleep(SLEEP_TIME)