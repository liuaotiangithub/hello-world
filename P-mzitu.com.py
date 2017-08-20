#多线程爬去Mzitu.com 的照片
#由于网站设置访问限制，访问过快会被检测是爬虫
#所以延迟两秒
import requests
from bs4 import BeautifulSoup
from time import sleep, ctime
import threading
import re
from atexit import register

URL = 'http://www.mzitu.com/'
URL_LIST = [99512, 92107] #如果想爬去其他网页，就在这里添加那个网页的后缀数字

def get_img(soup, number):
	data = soup.find_all('div', class_="main-image")
	re_ = re.compile("src=\"http://.+\.jpg")
	name = re.search(r"alt=\".+?\"", str(data)).group()[5:-1]
	data = re.search(re_, str(data)).group()[5:]  #正则出来的图片地址
	download_image(data, number, name)

def get_image(suf, n):
	for i in range(1,51): #控制每个网页爬去的数量
		url = ('%s%s/%s' % (URL,suf, i))
		sleep(4)
		r = requests.get(url)
		soup = BeautifulSoup(r.text, "html.parser")
		get_img(soup, i)
	

def download_image(url, id, name):
	r =requests.get(url)
	PATH = 'C:/Users/Liuaotian/Desktop/开发文件/美女图片/'  #图片保存的地址，也可更改
	path = ("%s%s%s%s" % (PATH, name, id, ".jpg"))
	with open(path, 'wb') as f:
		f.write(r.content)

def main():
	print("-" * 50)
	print('由于作者比较懒，所以懒得做网站列表(实际上已经做了，但由于接口问题\n就不发了,就请你手动查找想爬去mzitu网站后的\n数字，然后添加到URL_LIST也可以修改源码，达到控制数量的目的。)')
	input('好了，回车开始吧')
	threads = []
	nloops = range(len(URL_LIST))
	for i in nloops:
		#get_image(URL_LIST[i])
		t = threading.Thread(target=get_image, args=(URL_LIST[i], i))
		threads.append(t)
	for i in nloops:
		threads[i].start()
	for i in nloops:
		threads[i].join()

@register
def _atexit():
	print("All DONE at:", ctime())

if __name__ == "__main__":
	print("stacking at:", ctime())
	main()