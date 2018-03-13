import requests
from bs4 import BeautifulSoup
import os
from time import sleep

headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}


def Get_Url_Title():
    """
    返回一个li标签的列表
    :return:
    """
    print("进入Title")
    data = {}
    mzitu_url = "http://www.mzitu.com/"
    r = requests.get(mzitu_url)
    soup = BeautifulSoup(r.text, "html.parser")
    li_tag_list = soup.find("ul", id="pins").find_all("li")
    for i in li_tag_list:
        data[i.a.img["alt"]] = i.a["href"]
    return data

def Download_Image(r, url, count, referer):
    headerss = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        "Referer": "http://www.mzitu.com"}
    data = r.get(url, headers=headerss).content
    if data:
        with open((str(count) + ".jpg"), "wb") as f:
            f.write(data)
            print("写入成功")
            #下载之后休眠三秒
            sleep(3)
    else:
        print("请求失败")
def Get_Image_Url(url):
    """
    :param url:接受一个Page的URL
    :return:所有图片的地址
    """
    r =requests.Session()
    html = r.get(url)
    #先找到所有页数
    soup = BeautifulSoup(html.text, "html.parser")
    page = int(soup.find("div", class_="pagenavi").find_all("span")[-2].string)
    for i in range(0, page):
        #索取每一页，因为从0开始，所以每一个i 加1
        i += 1
        image_url = url + "/" + str(i)
        image_html = r.get(image_url) #每一页的HTML
        sleep(0.5)
        soup = BeautifulSoup(image_html.text, "html.parser")
        image_url = soup.find("div", class_="main-image").p.a.img["src"]
        Download_Image(r, image_url, i, url)




def Get_Page_Url(data):
    """
    :param data:
        接受一个字典
    :return:
        返回一个URL列表
    """
    for key in data:
        file_name = str(key).split()[0]  #以空格分开，因为ubuntu里文件名不能有空格
        current_path = os.getcwd() #获取当前文件夹，一会要在切换回来
        if os._exists(file_name):  #检测文件是否存在
            print(file_name, "文件已经创建", sep="")
            os.chdir(file_name)
        else:
            os.mkdir(file_name)
            os.chdir(file_name)
        Get_Image_Url(data[key])  #每次返回一个URL列表，然后返回出去
        os.chdir(current_path)




if __name__ == "__main__":
    data_dict = Get_Url_Title()
    Get_Page_Url(data_dict)
