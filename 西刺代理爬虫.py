import requests
from bs4 import BeautifulSoup
from time import sleep

Origin_Url = "http://www.xicidaili.com/nn/"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

for i in range(1, 101):
	print("正在爬取第{}页".format(i))
	url = Origin_Url + str(i)
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.text, "html.parser")
	tr_list = soup.find("table", id="ip_list").find_all("tr")[1:]
	for i in tr_list:
		td_list = i.find_all("td")
		ip = td_list[1].string
		port = td_list[2].string
		http = td_list[5].string
		with open("ip.txt", "a+") as f:
			data = "{}\t{}\t{}\n".format(ip, port, http)
			f.write(data)
	sleep(5)#休眠五秒，以尊重服务器 2333
