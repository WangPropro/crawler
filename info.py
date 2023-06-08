import requests as rqs
from lxml import etree
import pandas as pd

# 创建一个 Session 对象
# session = rqs.Session()
url = "https://yz.chsi.com.cn/zsml/queryAction.do?ssdm={ssdm}&dwmc={dwmc}&mldm={mldm}&mlmc={mlmc}&yjxkdm={yjxkdm}&zymc={zymc}&xxfs={xxfs}&pageno={pageno}"

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

params = {
    "ssdm": "33",
    # 31是上海市的代码
    # 32是江苏省的代码
    # 33是浙江省的代码
    "dwmc": "",
    "mldm": "08",    #zyxw
    "mlmc": "",
    "yjxkdm": "0812",
    "zymc": "",  # 人工智能,电子信息,计算机技术,大数据技术与工程
    "xxfs": "1",
    # 1是全日制
    # 2是非全日制
    "pageno": 1
}

# # 发送第一个请求
# response = session.get(url.format(**params))
# print(response.text)

# # 修改参数并发送第二个请求
# params["pageno"] = 2
# response = session.get(url.format(**params))
# print(response.text)

# # 关闭 Session 对象
# session.close()

result_table = []

def get_search_data(params: dict):
    return rqs.get(url.format(**params), headers=headers).content.decode("utf-8")

def get_a_record(url, schoolInfo: dict):
    data_xpath = etree.HTML(rqs.get("https://yz.chsi.com.cn" + url, headers=headers).content.decode("utf-8")) # type: ignore
    result_table.append({
        "院校名称": data_xpath.xpath("//table/tbody/tr[1]/td[2]/text()")[0],
        "研究生院": schoolInfo["gso"],
        "自主划线": schoolInfo["ao"],
        "博士点": schoolInfo["phd"],
        "考试方式": data_xpath.xpath("//table/tbody/tr[1]/td[4]/text()")[0],
        "院系所": data_xpath.xpath("//table/tbody/tr[2]/td[2]/text()")[0],
        "专业": data_xpath.xpath("//table/tbody/tr[2]/td[4]/text()")[0],
        "研究方向": data_xpath.xpath("//table/tbody/tr[3]/td[4]/text()")[0],
        "拟招人数": data_xpath.xpath("//table/tbody/tr[4]/td[4]/text()")[0],
        "政治": data_xpath.xpath("//div[@class=\"zsml-result\"]/table/tbody/tr/td[1]/text()")[0],
        "英语": data_xpath.xpath("//div[@class=\"zsml-result\"]/table/tbody/tr/td[2]/text()")[0],
        "业务课一": data_xpath.xpath("//div[@class=\"zsml-result\"]/table/tbody/tr/td[3]/text()")[0],
        "业务课二": data_xpath.xpath("//div[@class=\"zsml-result\"]/table/tbody/tr/td[4]/text()")[0]
    })

def get_a_school_data(url, schoolInfo: dict):
    data_xpath = etree.HTML(rqs.get("https://yz.chsi.com.cn" + url, headers=headers).content.decode("utf-8")) # type: ignore
    result = data_xpath.xpath("""//table/tbody/tr/td[8]/a/@href""")
    # 查看详细信息连接
    for i in result:
        get_a_record(i, schoolInfo)

def get_a_page_data(data):
    data_xpath = etree.HTML(data) # type: ignore
    school_names = data_xpath.xpath("""//*[@id="form3"]/a/text()""")
    # 院校名称
    mid_urls = data_xpath.xpath("""//*[@id="form3"]/a/@href""")
    # 中间网址，进一步访问院校该专业的搜索结果
    graduate_school_opt = data_xpath.xpath("""/html/body//table/tbody/tr/td[3]""")
    # 是否研究生院
    autonomous_opt = data_xpath.xpath("""/html/body//table/tbody/tr/td[4]""")
    # 是否是自主划线院校
    PhD_point_opt = data_xpath.xpath("""/html/body//table/tbody/tr/td[4]""")
    # 是否是博士点
    return [school_names, mid_urls, graduate_school_opt, autonomous_opt, PhD_point_opt]

def analysis_loop(data):
    data_xpath = etree.HTML(data) # type: ignore
    max_page_num = data_xpath.xpath("""/html/body//div[4]/ul/li/a/text()""")[-1]
    print('最大页数:', max_page_num)
    # 最大页数
    for k in range(1, int(max_page_num) + 1):
        global params
        params["pageno"] = k
        # print(params)
        apage = get_a_page_data(rqs.get(url.format(**params), headers=headers).content.decode("utf-8"))
        # print(apage[0][0])
        for s in range(len(apage[1])):
            schoolInfo = {}
            # 记录院校的研究生点、自主划线、博士点
            for i in range(2, 5):
                if len(apage[i][s].xpath("./i")) != 0:
                    schoolInfo[["gso", "ao", "phd"][i - 2]] = 1
                else:
                    schoolInfo[["gso", "ao", "phd"][i - 2]] = 0

            get_a_school_data(apage[1][s], schoolInfo)

if __name__ == "__main__":
    data = get_search_data(params)
    analysis_loop(data)
    df = pd.DataFrame(result_table)
    df.to_csv("大数据工程专业院校信息.csv", encoding="gbk", index=False)