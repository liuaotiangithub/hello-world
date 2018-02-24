import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint


if __name__ == "__main__":


	print("start")
	data_list = []
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"}

	for i in range(0, 20):
		i += 1
		print("loading...", i)
		URL = "http://www.xicidaili.com/wn/"
		URL = URL + str(i)
		r = requests.get(URL, headers=headers)
		soup = BeautifulSoup(r.text, "html.parser")

		#www.allsrc.cn
		table_tag = soup.find("table", id="ip_list")

		soup = BeautifulSoup(str(table_tag), "html.parser")
		tr_tag_list = soup.find_all("tr")[1:]
		for tr in tr_tag_list:
			ip_data_list = []
			soup = BeautifulSoup(str(tr), "html.parser")
			td_list = soup.find_all("td")
			#2   3   6
			ip_data_list.append(td_list[1].text)
			ip_data_list.append(td_list[2].text)
			ip_data_list.append(td_list[5].text)
			data_list.append(ip_data_list)
		sleep(2)
	print("ip get end...")
	url = input("请输入一个网站URL(http/https):")
	print("get url start...")
	#url = "https://www.allsrc.cn/other/WindowsNet.html"
	count = 0
	for i in data_list:
		count+=1
		print("Scanning...")
		http = "http://"+i[0]+":"+i[1]
		https = "https://"+i[0]+":"+i[1]
		proxies = {"http":http,
					"https":https}
		try:
			with open("log.log", "a+") as f:
				f.write(i[0])
				f.write("正在请求")
				f.write("\n")
			r = requests.get(url, proxies=proxies, timeout=5, headers=headers)
		except:
			continue
		if r.status_code == 200:
			with open("win.log", "a+") as f:
				f.write(i[0])
				f.write("Get成功----")
				f.write("总计成功--")
				f.write(str(count))
				f.write("-次\n")
			print("get win...")
		else:
			continue
		number = randint(1, 3)
		sleep(number)
