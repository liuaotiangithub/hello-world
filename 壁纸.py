import requests
from bs4 import BeautifulSoup
from random import randint
from platform import system
import os
import re
import ctypes

hand_url = "https://bing.ioliu.cn/"
print("Look for image...")
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
r = requests.get("https://bing.ioliu.cn/", headers=headers)  
#使用headers以表示尊重
soup = BeautifulSoup(r.text, "html.parser")
count = randint(0, 11)
div = soup.find_all("div", class_="item")[count]
url = hand_url + div.div.a["href"]
r = requests.get(url, headers=headers)
search_data = re.compile(r'data-progressive="(.*?)"')
image_url = search_data.findall(r.text)[0]
image = requests.get(image_url, headers=headers)
if system() == "Windows":
	#if system is Windows
	Path = "C://壁纸"
	if os.path.exists(Path):
		#if folder exist
		with open("C://壁纸/1.jpg", "wb") as f:
			f.write(image.content)
			print("download image file over!")
			#write file
	else:
		#if folder not exist
		os.mkdir(Path)
		with open("C://壁纸/1.jpg", "wb") as f:
			f.write(image.content)
			print("download image file over!")
			#write file
	ctypes.windll.user32.SystemParametersInfoW(20, 0, "C://壁纸/1.jpg", 0)
	print("End of setting!")
elif system() == "Linux":
	#if system is Linux
	Path = "/home/壁纸"
	if os.path.exists(Path):
		#if folder exist
		with open("/home/壁纸/1.jpg", "wb") as f:
			f.write(image.content)
			print("download image file over!")
			#write file
	else:
		#if folder not exist
		os.mkdir(Path)
		print("mkdir folder in ", os.getcwd())
		with open("/home/壁纸/1.jpg", "wb") as f:
			f.write(image.content)
			print("download image file over!")
			#write file

	os.system('gsettings set org.gnome.desktop.background picture-uri "file:/home/壁纸/1.jpg"')
	print("End of setting!")
else:
	#not know system
	print("not know system!")