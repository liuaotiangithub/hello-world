from bs4 import BeautifulSoup
import requests
import re
import os
def main():
	URL = 'tianqi.com'
	print('欢迎使用天气查询目前支持查询市级和省级.')
	trr = input('请输入你想查询城市名(拼音):')
	trr = 'http://' + trr + '.' + URL  #组合成请求的网页
	try:
		r = requests.get(trr)
	except:
		print('请求失败')
		return
	data = r.text
	soup = BeautifulSoup(data, 'html.parser')
	wendu = soup.find_all('')
	#data = soup.find_all('div', class_="temp")
	data = soup.find_all('h3')
	data = data[2]
	data = list(data)
	wendushidu = soup.find_all('div', id='rettemp')
	wendushidu = str(wendushidu)
	re1 = r'\d{0,3}\.\d{1,2}\°' #匹配温度
	re2 = r'相对湿度：\d{0,3}\%'
	re1_data = re.search(re1, wendushidu)
	re2_data = re.search(re2, wendushidu)
	try:
		print(data[0] + ':' + re1_data.group())
		print(data[0][:4] + '湿度:' + re2_data.group())
	except:
		os.system('cls')
		print("未找到该信息，请及时联系管理员q:1151172004")
if __name__ == '__main__':
	while (True):
		main()