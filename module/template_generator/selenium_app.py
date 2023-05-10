from time import sleep
from config_generator.webdriver_config import selenium_start, webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import os,json
from selenium.webdriver.common.keys import Keys
import pyperclip
def start():
    return selenium_start()

def get_url(seldrv = start(),url:str=None):
	seldrv.get(url)
	return seldrv

def login(elem):
	elem.find_element(By.XPATH,'//*[@id="UserName"]').send_keys("m.oguenko@apkipp.ru")
	elem.find_element(By.XPATH,'//*[@id="Password"]').send_keys("M@kstiv4erazavtrabudeshspat")
	elem.find_element(By.XPATH,'//*[@id="SubmitCredentials"]').click()


def on_folder_page(drv:WebDriver,delay:int = 30):
	try:
		element_onpage_present = EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[3]/div[5]/div/div/div[1]/div[1]/div/div[1]/div/a'))
		on_page = WebDriverWait(drv, delay).until(element_onpage_present)
		top_element = on_page.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[3]/div[5]/div/div/div[1]/div[1]/div/div[1]/div/a')
		text = top_element.text
		if text:
			top_element.click()
			on_topelement_page(drv)
		return text
	except TimeoutException:
		print ("[on page] Loading took too much time!")


def on_topelement_page(drv:WebDriver,delay:int = 30):
	try:
		element_onpage_click_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="horizontal-menu"]/div/div[1]/div/ul/li[2]/button/span[2]'))
		onpage_click_elem = WebDriverWait(drv, delay).until(element_onpage_click_elem)
		on_top_element_text = onpage_click_elem.find_element(By.XPATH,'//*[@id="ReactRouter"]/div/div/div/div/div/div[1]/h1').text
		print("ontop",on_top_element_text)
		onpage_click_elem.find_element(By.XPATH,'//*[@id="horizontal-menu"]/div/div[1]/div/ul/li[1]/a').click()

		onpage_url_change = WebDriverWait(drv,delay).until(EC.url_contains("edit"))

		if onpage_url_change:

			path = f"{os.getcwd()}\\module\\template_generator\\ready\\sport\\Sport_all\\pk"
			list_files = os.listdir(f"{os.getcwd()}\\module\\template_generator\\ready\\sport\\Sport_all\\pk")
			with open(os.path.join(f"{os.getcwd()}\\","theme_text.json"),'r',encoding='utf-8') as f:
				theme_data = json.loads(f.read())
			count = 0
			for theme in theme_data:

				for file in list_files[111:]:
					name = file.replace(".html","").replace("[ПК] [ОС] ","")
					title = file.replace(".html","")
					if theme.get("specname") == name:
						print(file)
						count+=1
						with open(os.path.join(f"{path}",file),'r',encoding='utf-8') as f:
							if theme.get("valid"):
								js = {
									"title": title,
									"theme_text": theme.get("text"),
									"content": f.read()
								}
							else:
								js = {
									"title": f"[!] {title}",
									"theme_text": theme.get("text"),
									"content": f.read()
								}
							try:
								element_onpage_click_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="mailing"]/div/div/div[2]/div/div/div[3]/div/div[1]'))
								onpage_click_elem = WebDriverWait(drv, delay).until(element_onpage_click_elem)
								a = ActionChains(drv)
								a.move_to_element(onpage_click_elem.find_element(By.XPATH,'//*[@id="mailing"]/div/div/div[2]/div/div/div[3]/div/div[1]')).perform()
								sleep(1.2)
								a.click(onpage_click_elem.find_element(By.XPATH,'//*[@id="mailing"]/div/div/div[2]/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div/div/button')).perform()

								# Select all text in editor
								a.double_click(onpage_click_elem.find_element(By.XPATH,'//*[@id="brace-editor"]/div[2]/div')).double_click().perform()
								# a.send_keys(f"{js['content']}").perform()
								pyperclip.copy(js["content"])
								a.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
								sleep(1)

								# save template
								a.click(onpage_click_elem.find_element(By.XPATH,'//*[@id="save-html-template-button"]')).perform()
								sleep(7.5)
								try:
									element_onBackpage_ = EC.presence_of_element_located((By.XPATH, '//*[@id="mailing"]/div/div/div[2]/div/div/div[1]/div/div/div'))
									onpage_click_elem_ = WebDriverWait(drv, delay).until(element_onBackpage_)
									sleep(1)
									a.reset_actions()
									a.click(onpage_click_elem_.find_element(By.XPATH,'//*[@id="mailing"]/div/div/div[2]/div/div/div[1]/div/div/div')).double_click().perform()
									a.send_keys(f"{js['theme_text']}").perform()
									a.move_to_element(onpage_click_elem.find_element(By.XPATH,'//*[@id="mailing"]/div/div/div[1]/div/div')).click().perform()
									sleep(3)
									a.click(onpage_click_elem.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div')).double_click().perform()
									a.send_keys(f"{js['title']}").perform()
									sleep(1)
									a.click(onpage_click_elem.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/button')).perform()
									a.move_to_element(onpage_click_elem.find_element(By.XPATH,'//*[@id="mailing"]/div/div/div[1]/div/div')).click().perform()
									sleep(2)
									a.click(onpage_click_elem.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[1]/div/div[3]/div/button[1]')).perform()
									sleep(2)
									# duplicate button
									a.click(onpage_click_elem.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[1]/div/div[3]/div/button[2]/span[1]')).perform()
									sleep(3)
								except TimeoutException:
									print("[on back page] Loading took too much time!")
							except TimeoutException as e:
								print(f"erro {e}")
			print("SAVE ALL SHIT")
	except TimeoutException:
		print ("[onpage_click_elem] Loading took too much time!")

def main():
	sel_page = get_url(url="https://apkipp.mindbox.ru/newcampaigns/email-mailings?folder=92d81c3b-c832-46c1-b768-8875a6731161")

	# sel_page.find_element(By.ID,"UserName")
	delay = 80
	try:
		element_login_present = EC.presence_of_element_located((By.ID, 'UserName'))
		login_el = WebDriverWait(sel_page, delay).until(element_login_present)
		login(login_el)

		url_change = WebDriverWait(sel_page,delay).until(EC.url_contains("folder=92d81c3b-c832-46c1-b768-8875a6731161"))
		if url_change:
			on_folder_page(sel_page,delay)

		print(f"Page is ready!{sel_page}")
	except TimeoutException:
		print ("[login page] Loading took too much time!")

def load_file():
	path = f"{os.getcwd()}\\module\\template_generator\\ready\\sport\\Sport_all\\pk"
	list_files = os.listdir(f"{os.getcwd()}\\module\\template_generator\\ready\\sport\\Sport_all\\pk")
	with open(os.path.join(f"{os.getcwd()}\\","theme_text.json"),'r',encoding='utf-8') as f:
		theme_data = json.loads(f.read())
	count = 0
	for theme in theme_data[41:]:

		for file in list_files:
			name = file.replace(".html","").replace("[ПК] [ОС] ","")
			title = file.replace(".html","")
			if theme.get("specname") == name:
				count+=1
				with open(os.path.join(f"{path}",file),'r',encoding='utf-8') as f:
					js = {
						"title": title,
						"theme_text": theme.get("text"),
						"content": f.read()
					}
					print(js['title'])

if __name__ == "__main__":
    main()
	# load_file()