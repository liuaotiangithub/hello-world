from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys


def loginAndOpen(Qq, username, passworld):
	#Qq = webdriver.Chrome()
	Qq.get("https://qzone.qq.com/")
	Qq.switch_to.frame("login_frame")
	Qq.find_element_by_id("switcher_plogin").click()
	Qq.find_element_by_id("u").send_keys(username)
	Qq.find_element_by_id("p").send_keys(passworld)
	Qq.find_element_by_id("login_button").click()
	sleep(30)#测试时可以手动点击
	#sleep(5)  #测试时手动改点击五秒足矣
	#登录时由于某些用户选取了加载界面的话，睡眠30s用于画面跳过
	Qq.find_element_by_id("aIcenter").click()
	sleep(1)
	print("开始")

def get_chrome():
	return webdriver.Chrome()

def dianzan(Qq, ypix, i):
	try:
		xpath = '//*[@id="feed_friend_list"]/li[%d]/div[3]/div[1]/p/a[3]/i' % i
		pdxpath = '//*[@id="feed_friend_list"]/li[%d]/div[3]/div[1]/p/a[3]' % i #判断是否已经点赞的地址
		if Qq.find_element_by_xpath(pdxpath).get_attribute("class") == "item qz_like_btn_v3 item-on":
			#等于这个说明已经点赞了
			return False
		Qq.find_element_by_xpath(xpath).click()
	except Exception as e:
		print(i,"处出现错误，请排查错误原因")
		return False
	Qq.execute_script("window.scrollTo(0, %d);" % ypix)
	sleep(1)
	return True
def miaoping(Qq, i):
	try:
		Qq.find_element_by_xpath('//*[@id="fct_1072912774_311_0_1511694253_0_1"]/div[3]/div[4]/div/div/div/div[1]').send_keys("Mz -----刘傲天!")
		
	except Exception as e:
		raise e


def click_1(Qq, send_data):  #点赞函数
	ypix = 1000
	Qq.execute_script("window.scrollTo(0, %d);" % ypix)
	for i in range(1, 6):
		if dianzan(Qq, ypix, i):
			pinglun(Qq, i, send_data)
		ypix+=800
		sleep(1)
		print("翻页")

def set_chrome(user_agent):
	options = webdriver.ChromeOptions()
	options.add_argument('lang=zh_CN.UTF-8')
	options.add_argument(user_agent)
	return webdriver.Chrome(chrome_options=options)

def set_send(recv_string='Mz---!'):
	return recv_string

def main():
	#set_charome提供设置请求头功能更
	handle = get_chrome()

	loginAndOpen(handle, "username", "password")
	send_data = set_send('刘哥到此一游!')  #set_send设置评论的文字
	while (True):
		click_1(handle, send_data)
		sleep(10)
		print("休眠结束")
		handle.refresh()

def pinglun(Qq, i, send_data):
	sleep(2)
	print("评论")
	path = '//*[@id="feed_friend_list"]/li[%d]' % i
	idpath = Qq.find_element_by_xpath(path).get_attribute('id')
	#Qq.find_element_by_xpath('//*[@id="fct_997962031_311_5_1511866865_0_1"]/div[3]/div[4]/div[2]/div/div/div[2]/a/i').click()
	for count in range(2, 5):
		path = ('//*[@id="%s"]/div[3]/div[%d]/div/div/div/div[2]/a/i' % (idpath, count))
		try:
			print("path:", path)
			Qq.find_element_by_xpath(path).click()	
			break
		except Exception as e:
			continue
	sleep(3)
	try:
		Qq.find_element_by_id("$2_content_content").send_keys(send_data)
		Qq.find_element_by_id("$2_content_content").send_keys(Keys.CONTROL, Keys.ENTER)
	except Exception as e:
		pass
	
if __name__ == "__main__":
	main()