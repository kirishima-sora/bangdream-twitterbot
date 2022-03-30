from selenium import webdriver
import time

username = "Q6GUVp50d67dlx0"
password = "5k8r5hdr"

url = "https://twitter.com/i/flow/login"

#twitterログイン画面へのアクセス
driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)

#username入力⇒次へボタン押下
username_form = driver.find_element_by_name("text")
username_form.send_keys(username)
driver.find_element_by_xpath("//*[text()=\"次へ\"]").click()

#ページ切り替わり待ち
time.sleep(5)

#password入力⇒ログインボタン押下
password_form = driver.find_element_by_name("password")
password_form.send_keys(password)
#ログインボタンのアクティブ待ち
time.sleep(3)
driver.find_element_by_xpath("//*[text()=\"ログイン\"]").click()




time.sleep(5)
driver.quit()

