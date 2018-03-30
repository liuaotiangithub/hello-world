import requests
from bs4 import BeautifulSoup

url_path = "http://weixin.sogou.com/weixin?type=2&query={}&page={}"
page = 1  #Get Data Pages
Url_List = [] #Save Url Content
Get_Data = "互联网"#Get Data KeyWords
#config

Headers = {"Uset-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
def Get_Url_Html(url):
	return requests.get(url, headers=Headers).text

def Resolve_Html(html):
	soup = BeautifulSoup(html, "html.parser")
	All_Div_Tags = soup.find_all("div", class_="txt-box")
	#Search All div tags of ul.li
	for data in All_Div_Tags:
		#resolve div tags
		Article_content = []
		#Get a tag string content
		Article_content.append(data.h3.a.get_text())
		Article_content.append(data.h3.a["href"]) #Get Article Url	
		Url_List.append(Article_content)

def Resove_Article_Html(html):
	soup = BeautifulSoup(html, "html.parser")
	div_content = soup.find("div", id="js_content")
	while True:
		try:
			div_content.section.decompose() #delete section DOM
		except Exception as e:
			break
	return div_content.get_text()
		

if __name__ == "__main__":
	
	for i in range(0, page):
		Search_url = url_path.format(Get_Data, i+1)
		#because i first 0, so i + 1
		Resolve_Html(Get_Url_Html(Search_url))
		#print(Url_List)
		for url in Url_List:
			title = url[0]
			print(title)
			print(Resove_Article_Html(Get_Url_Html(url[1])).replace("。", "。\n"))
			break
