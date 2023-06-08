import csv
import requests
from lxml import etree
from time import sleep

headers = {
    'Cookie':
    # 'user_trace_token=20221116090352-d4642eeb-afa6-444c-82bf-097ffb450be3 LGUID=20221116090402-8151b708-5794-4af7-8c08-52b3bf366bd8; _ga=GA1.2.2070149427.1668560644; RECOMMEND_TIP=true; X_HTTP_TOKEN=74a293c4a1faa8b962747096611e97668ea21715c6; WEBTJ-ID=20221122075210-1849c9b3c323b3-0b7f343075f0df-26021e51-2073600-1849c9b3c335d9; JSESSIONID=ABAAAECABIEACCA5BEDD9FD6A6D1ADE87560B16FD6D6C45; sensorsdata2015session={}; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1668597745,1668867849,1668911464,1669074781; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1669074781; LGRID=20221122075300-c46e57de-5c1b-4e4e-af71-7367c31321c4; _putrc=40325B91DBC99EB9123F89F2B170EADC; login=true; hasDeliver=0; privacyPolicyPopup=false; __lg_stoken__=4cf3815c9d06f2465bf54b078c0dbe39ae509f4a327589bad909d9a06b9611212010f999d165ee1ce1367be26eaa093cc7fa50448326c4dc94243c28ec0facd2216a4a51e4b3; sm_auth_id=pveghccxnc73sd89; gate_login_token=01ada8dfe8e5e2cea6dafb45a55f5b0fa858a6696bdeee1da3a940ae5cdcdc03; sensorsdata2015jssdkcross={"distinct_id":"1847df6ed77787-00818d43933adc-26021e51-2073600-1847df6ed78bba","$device_id":"1847df6ed77787-00818d43933adc-26021e51-2073600-1847df6ed78bba","props":{""$latest_referrer":"","$os":"Windows","$browser":"Chrome","$browser_version":"113.0.0.0"}}',
    'user_trace_token=20221116090352-d4642eeb-afa6-444c-82bf-097ffb450be3; LGUID=20221116090402-8151b708-5794-4af7-8c08-52b3bf366bd8; _ga=GA1.2.2070149427.1668560644; RECOMMEND_TIP=true; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1685580107; LG_HAS_LOGIN=1; hasDeliver=0; privacyPolicyPopup=false; index_location_city=%E5%8C%97%E4%BA%AC; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; __lg_stoken__=05dea4d3681464c10450dbf96bfad34593ee7f648a461ca55c054b2a40950819e94d4cdb66403bcf2fb9601ee1e283c68879bb0f016dc85a3a01000844cc96a3a2b92207a9c9; X_HTTP_TOKEN=74a293c4a1faa8b949274958611e97668ea21715c6; WEBTJ-ID=20230605144134-1888a4a245a5fa-0356bd4ac4fc4f-26031d51-1764000-1888a4a245bc5a; JSESSIONID=ABAAABAABEIABCI1E6BB0F36DAE2F29AD6A26C6BDFF7BD7; sensorsdata2015session=%7B%7D; gate_login_token=v1####2940650de4cf90b0d43da362b12b85686b39849151188a3ddc032dc6e0024e80; LG_LOGIN_USER_ID=v1####5e08fbe3fee05472d30dc28ff5ab3a59f5b6b2d13238bafef2ab8532e0126be8; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2226170386%22%2C%22first_id%22%3A%2218874669957517-05b6925bb3d4a-26031d51-1764000-18874669958711%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%22114.0.0.0%22%7D%2C%22%24device_id%22%3A%2218874669957517-05b6925bb3d4a-26031d51-1764000-18874669958711%22%7D',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    'Chrome/113.0.5672.127 Safari/537.36'
}

def get_info_job(job_url):
    response = requests.get(url=job_url, headers=headers).text
    selector = etree.HTML(response) # type: ignore
    lis = selector.xpath('//*[@id="jobList"]/div[1]/div')

    for li in lis:
        name_area = li.xpath('.//div[1]/div[1]/div[1]/a/text()')
        print(name_area)
        title = name_area[0]
        print(title)
        area = name_area[1].replace('[', '').replace(']', '')
        print(area)

        sleep(2)
        
        salary = li.xpath('.//div[1]/div[1]/div[2]/span/text()')[0]
        # print(salary)
        try:
            exp_degree = li.xpath('.//div[1]/div[1]/div[2]/text()')[0]
        except IndexError:
            exp_degree = '无要求'
        # print(exp_degree)
        tags = li.xpath('.//div[2]/div[1]/span/text()')
        if not tags:
            tags = '/'
        # print(tags)
        company_name = li.xpath('.//div[1]/div[2]/div[1]/a/text()')[0]
        # print(company_name)
        try:
            company_Type_Size = li.xpath('.//div[1]/div[2]/div[2]/text()')[0]
        except IndexError:
            company_Type_Size = '/'
        print(company_Type_Size)
        try:
            benefits = li.xpath('.//div[2]/div[2]/text()')[-1].replace('“', '').replace('”', '')
        except IndexError:
            benefits = '/'
        job_datas = {
            '职位名称': title,
            '地区': area,
            '薪水': salary,
            '经验和学历要求': exp_degree,
            '工作标签': tags,
            '公司名称': company_name,
            '公司类别和规模': company_Type_Size,
            '福利待遇': benefits
        }
        print(job_datas)
        writer.writerow([
            title,
            area,
            salary,
            exp_degree,
            tags,
            company_name,
            company_Type_Size,
            benefits
        ])


if __name__ == '__main__':
    # 打开一个CSV文件，并插入表头信息
    f = open('拉钩网python大数据.csv', mode='a', encoding='utf-8', newline='')
    writer = csv.writer(f)
    writer.writerow([
        '职位名称',
        '地区',
        '薪水',
        '经验和学历要求',
        '工作标签',
        '公司名称',
        '公司类别和规模',
        '福利待遇'
    ])

    # 爬取1-30页的内容
    for page in range(1, 31):
        url = f'https://www.lagou.com/wn/jobs?pn={page}&fromSearch=true&kd=大数据'
        if page == 1:
            print(f'正在爬取{page}页......')
        if page > 1:
            print('\n')
            print(f'正在爬取{page}页......')

        # 爬取一页信息内容并写入到CSV文件内
        get_info_job(url)

        # 爬取下一页的时候等待2秒
        sleep(2)
    f.close()

    def get_info_job(job_url):
        response = requests.get(url=job_url, headers=headers).text
        print(response)
