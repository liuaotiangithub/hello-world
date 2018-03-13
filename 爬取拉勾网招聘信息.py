import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint

Search_data = []#存储所有搜索到的数据
Headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
           "Host": "www.lagou.com"}
#先写一个获取页面
def Get_Python_Page(search_data = "Python",page = 1):
    """
    :param page:页数
    :return: 当前页的招聘的URL
    """
    url_list = []
    r = requests.get(("https://www.lagou.com/zhaopin/{}/{}/?filterOption=3".format(search_data, page)), headers=Headers)
    #获取这个页面，找到每一家公司
    soup = BeautifulSoup(r.text, "html.parser")
    a_tag_data = soup.find_all("a", class_="position_link")
    #找到所有class等于这个的标签
    for i in a_tag_data:
        url_list.append(i["href"])

    return url_list

def Get_Page_Url_data(url):
    """
    :param url:接受每一页的URL请求
    :return: 返回想要的数据
    """
    try:
        #记录每一页的数据
        Page_data = {}
        r = requests.get(url, headers=Headers)
        soup = BeautifulSoup(r.text, "html.parser")
        #找找class等于name的span标签
        title = soup.find("span", class_="name").get_text()
        Page_data["标题"] = title
        #先把标题放进去
        tags = soup.find("dd", class_="job_request")
        span_tags = tags.find_all("span")#找到待遇
        li_tags = tags.find_all("li")#找到标签
        p_tags = tags.find_all("p")[-1].get_text().replace("\xa0", "")#找到最后一个p标签，也就是发布时间
        Job_have = soup.find("dd", class_="job-advantage").get_text()#找到职位诱惑
        Page_data["职位诱惑"] = Job_have
        Job_miaoshu = soup.find("dd", class_="job_bt").get_text().replace("\n\n", "\n")#找到职位描述
        Page_data["职位描述"] = Job_miaoshu
        Job_Address = soup.find("div", class_="work_addr").get_text().replace(" ", "").replace("\n", "")
        Page_data["工作地点"] = Job_Address[:-4]#去掉查看地图
        Job_HR = soup.find_all("span", class_="name")[-1].get_text() #获取文本内容
        Page_data["HR"] = Job_HR
        data = []
        for i in span_tags:
            data.append(i.get_text())#获得所有的要求
        Page_data["待遇"] = data
        data = []
        for i in li_tags:
            data.append(i.get_text())
        Page_data["标签"] = data
        Page_data["发布时间"] = p_tags

        return (Page_data, 0)
    except:
        print("被禁止访问了,即将休眠20秒")
        sleep(60)
        return (Page_data, 1)
        #如果出错返回1


def Find_Job(Job="Python", Page=1):
    """
    :param Job:需要查询的工作名称
    :param Page: 需要查询的页数
    :return: 返回json列表
    """
    Job_data = [] #职位数据
    url_list = Get_Python_Page(Job, Page)
    for url in url_list:
        number = randint(0, 5)
        data, status = Get_Page_Url_data(url)
        #如果出现错误，就休眠再次请求
        if status == 1:
            print("loading...五秒后将再次进入")
            sleep(5)
            print("再次进入被禁止访问的URL...")
            data, status = Get_Page_Url_data(url)
            if status == 1:
                print("唉，无能为力了，我们还是放弃吧，即将进行下一个...")
            else:
                print(data)
                Job_data.append(data)
        else:
            print(data)
            Job_data.append(data)
            #打印数据并放进列表
        #随机休眠避免被杀掉
        sleep(number)
    return Job_data
if __name__=="__main__":
    Find_Job("C++", 1)

