"""
	By:刘傲天
	time:2017-8-25
	功能:爬取纵横中文网月票排行榜，未用于商业用途，只是用来学习。
"""
import requests
from bs4 import BeautifulSoup
from sys import exit
import re

URL_DICT = {
	"月票榜":"http://book.zongheng.com/ranknow/male/r1/c0/q0/1.html",
	"点击榜":"http://book.zongheng.com/rank/male/r4/c0/q0/1.html",
	"新书榜":"http://book.zongheng.com/rank/male/r14/c0/q0/1.html",
	"红票榜":"http://book.zongheng.com/rank/male/r7/c0/q0/1.html",
	"黑票榜":"http://book.zongheng.com/rank/male/r10/c0/q0/1.html",
	"捧场榜":"http://book.zongheng.com/rank/male/r133/c0/q0/1.html",
	"潜力大作榜":"http://book.zongheng.com/rank/male/r12/c0/q0/1.html",
	"今日畅销榜":"http://book.zongheng.com/rank/male/r2/c0/q0/1.html",
	"新书订阅榜":"http://book.zongheng.com/rank/male/r13/c0/q0/1.html",
	"热门作品更新榜":"http://book.zongheng.com/rank/male/r16/c0/q0/1.html",
}
#排行榜URL地址。
URL = URL_DICT['月票榜']
old_data_list = []  #存储爬出来的结果
#拿到这个网站的soup解析过后的网页源代码
def return_url_text(url):
	try:
		r = requests.get(url)
	except:
		print('请求', url, '失败!')
		exit()
	return BeautifulSoup(r.text, "html.parser")

#将拿到的结果再次转换为beautifulsoup对象，之后再次解析
def zh_BS_object(data):
	return BeautifulSoup(str(data), "html.parser")

def li_get_data(li):
	for i in li: #对每个li进行操作
		re_get_span(i)  

def re_get_span(li):  #span_class是一个列表
	data = li_get_span(li) #接受返回的span列表
	#出现问题，每次都是天骄战纪
	data_list = []
	try:
		soup = zh_BS_object(data[0])  #第一个re的span
		data_list.append(soup.a['title']) #返回这个span的title
		soup = zh_BS_object(data[1]) #第二个re的span
		data_list.append(soup.span.string)
		soup = zh_BS_object(data[2])
		data_list.append(soup.a.string)
	except:
		data_list = []
		return
	old_data_list.append(data_list)

#由这个函数返回相应的span然后在用正则爬去
def li_get_span(li):
	span_list = []
	li = str(li).replace('\n', '')
	try:
		span_list.append(re.search(r'<span class="chap">.*?</span>', li).group())
		span_list.append(re.search(r'<span class="bit">.*?</span>', li).group())
		span_list.append(re.search(r'<span class="author">.*?</span>', li).group())
	except:
		span_list = []
		span_list = ['空', '空', '空']

	return span_list

def get_leibie(soup):
	leibie_list = []
	leibie_list.append('书名')
	data = BeautifulSoup(str(soup.find_all('span', class_="bit")), 'html.parser')
	leibie_list.append(re.search(r'<span class="bit">(.*?)</span>', str(data)).group(1))
	leibie_list.append('作者')
	old_data_list.append(leibie_list)

#解决输出对齐问题
def myAlign(string1, length=0):  
	count = 0
	for i in string1:
		if i >= '\u4300' and i <= '\u9fa5':
			count+=1
	number = length - (count * 2)
	data = ("%s%s" % (string1, ' '*number))
	return str(data)
def main():
	soup = return_url_text(URL)
	ul_data = soup.find_all('ul', class_='main_con') #将这个ul拿出来
	data = zh_BS_object(ul_data)  #将解析出来的文本再次放进去，拿到soup对象
	li_data = data.find_all('li')  #对新拿到的对象解析li标签。
	get_leibie(soup)
	li_get_data(li_data)   #塞进函数给他遍历出每个li的span对应的参数
	for i in old_data_list:
	 	print(myAlign(i[0], 20) + myAlign(i[1], 10) + myAlign(i[2], 10))
	#old_data_list就是爬来的数据，可以选择放到文件中，也可以选择输出

if __name__ == "__main__":
	main()