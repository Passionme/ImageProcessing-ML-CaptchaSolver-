#v4.0

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time
import os
import urllib.request
from PIL import Image
import numpy
import cv2
import pytesseract

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

global attempts, start, end, browser

options = Options()
options.add_argument("--enable-extensions")
options.add_argument("user-data-dir=C:\Profiles")
ext_path = r"C:\Users\Rajyam\AppData\Local\Google\Chrome\User Data\Default\Extensions\dhdgffkkebhmkfjojejmpbldmpobfkfo\4.8_0"
# options.add_extension(ext_path)
options.add_argument('--load-extension='+r"C:\Users\Rajyam\AppData\Local\Google\Chrome\User Data\Profile 4\Extensions\4.8_0")
options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application"
desktop = os.path.expanduser("~\Desktop\Profiles")
chromedriver = (os.path.join(r"C:\anaconda3\Lib\site-packages\chromedriver", 'chromedriver.exe'))
url =  "https://onlinebooking.sand.telangana.gov.in/MASTERS/HOME.ASPX"
browser = webdriver.Chrome(executable_path=chromedriver)




for file in os.listdir(desktop):
	shortcut = (os.path.join(desktop, file))
	print(os.path.join(desktop, file))


	def AutoLogin():
		global attempts,start, end, browser
		attempts += 1
		# browser.set_window_size(100, 70)


		#("Reading captcha")
		try:
			browser.get(url)
			image = browser.find_element_by_xpath("//img[@id ='ccMain_imgCaptcha']")
			src = (image.get_attribute('src'))
			urllib.request.urlretrieve(src, "captcha_img.bmp")
			x = Image.open( 'captcha_img.bmp').convert('RGB')
			# enlarge_size = tuple(2 * y for y in x.size)
			# x = x.resize(enlarge_size, Image.ANTIALIAS)
			open_cv_image = numpy.array(x)
			# Convert RGB to BGR
			open_cv_image = open_cv_image[:, :, ::-1].copy()
			cv2.imwrite("cap.bmp",open_cv_image)


			#("In CaptchaFind")
			captcha_img = cv2.imread("cap.bmp", cv2.IMREAD_COLOR)
			gray = cv2.cvtColor(captcha_img, cv2.COLOR_BGR2GRAY)

			lower = numpy.array([127,127,127 ])  # -- Lower range --
			upper = numpy.array([255, 255, 255])  # -- Upper range --
			mask = cv2.inRange(captcha_img, lower, upper)
			cv2.imwrite("mask.bmp",mask)

			res = cv2.bitwise_and(captcha_img, captcha_img, mask=mask)  # -- Contains pixels having the gray color--
			cv2.imwrite("inrange.bmp",res)


			kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))
			morph = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

			# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
			# morph2 = cv2.morphologyEx(morph, cv2.MORPH_DILATE, kernel)

			cv2.imwrite("morph.bmp",morph)
			# cv2.imwrite("morph2.bmp",morph2)


			text = pytesseract.image_to_string(Image.open("morph.bmp"), lang='eng', \
				config='--psm 3 --oem 3 -c tessedit_char_whitelist=123456789ABCDEF')
			import re

			regex = re.compile('[^A-Z0-9]')
			text = regex.sub('', text)
			print("text", text)

			if text:
				browser.find_element_by_xpath("//input[@type='text']").send_keys("9494197017")
				browser.find_element_by_xpath("//input[@type='password']").send_keys("12345678")
				browser.find_element_by_id("ccMain_txtEnterCode").send_keys(text)
				time.sleep(1)
				browser.find_element_by_id("btnLogin").click()
				# inputElement.send_keys(Keys.ENTER)
				# inputElement = browser.find_element_by_id("ccMain_txtEnterCode")
				# inputElement.send_keys(text)
				# inputElement.send_keys(Keys.ENTER)
				# inputElement.submit()

				print("Re-Check Captcha")
				try:
					WebDriverWait(browser, 1).until(EC.alert_is_present(), 'Waiting for alert timed out')
					alert = browser.switch_to.alert
					alert.accept()
					time.sleep(1)
					AutoLogin()
				except TimeoutException:
					pass
				try:
					print(browser.find_element_by_id("lblCustomerName").text)
					end = time.time()
					print("Log-in success in ", ((end - start)%60 ) - (2 * attempts), " sec", "and in ", attempts, " attempts")
					return
				except:
					try:
						if (browser.find_element_by_id("ccMain_tblLogOut").text):
							browser.find_element_by_id("btnLogout")
							end = time.time()
							print("Already Logged-in")
							print("Log-in success in ", ((end - start) % 60) - (2 * attempts), " sec", "and in ", attempts,
							  " attempts")
							return
						else:
							browser.find_element_by_id("ccMain_txtEnterCode")
							AutoLogin()

					except:
						browser.find_element_by_id("ccMain_txtEnterCode")
						AutoLogin()


			else:
				print("Re-Login")
				AutoLogin()
		except Exception as e:
			print(e)

	while(1):
		start = time.time()
		attempts = 0
		AutoLogin()
		time.sleep(30)  #wait till time to logout
