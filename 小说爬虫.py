import requests
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
Data = {}
#因为字典是无序的，这里保存一个有序的title
Title_list = []

def Get_Html(url):
	return requests.get(url, headers=headers).text

def Get_Data_In_Html(html):
	soup = BeautifulSoup(html, "html.parser")
	div = soup.find_all("div", class_="in")[-1]
	title = div.h3.string
	p = div.find_all("p")
	data = ""
	for i in p:
		if i.string:
			data += i.string + "\n"
	Data[title] = data
	Title_list.append(title)
	#获取完数据后检查是否是最后一章节
	span = soup.find("div", class_="page").find_all("span")[1]
	if span.a.string == "下一页":
		#如果第二个span的文本内容是下一页，就说明还有下一页
		print("下一页----", span.a["href"])
		return Get_Data_In_Html(Get_Html(span.a["href"]))
	else:
		return None  #实际上不用写这个else



def main():
	url = "http://book.jrj.com.cn/book/book/detail_62691.shtml" #第一章的地址
	html = Get_Html(url)
	Get_Data_In_Html(html)
	for i in Title_list:
		print(i, "----", Data[i])




if __name__ == "__main__":
	main()