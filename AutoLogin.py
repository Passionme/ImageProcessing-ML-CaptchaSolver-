#v3.0
from bs4 import BeautifulSoup
import urllib
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import urllib.parse as  urlparse
import time
from PIL import Image
import cv2
import numpy

def readurl_captcha(username="8639082347", password="12345678" ):

    # Retreive the captcha
    url = "https://onlinebooking.sand.telangana.gov.in/MASTERS/HOME.ASPX"

    try:
        content = urllib2.urlopen(url)
        # print(content)
        data = BeautifulSoup(content, "lxml")
        # print(data)
        error = (data.find('img', id="Img1"))
        # print("Error",error)
        if error:
            error_msg = data.find('span', id='lblNote')
            print(error_msg)
        else:
            captcha = data.find('img', id='ccMain_imgCaptcha')
            urllib2.urlretrieve(urlparse.urljoin(url, captcha['src']), 'captchaimg.bmp')
            x = Image.open( 'captchaimg.bmp').convert('RGB')
            open_cv_image = numpy.array(x)
            # Convert RGB to BGR
            open_cv_image = open_cv_image[:, :, ::-1].copy()
            cv2.imwrite("cap.bmp",open_cv_image)

    except Exception as e:
        print("Error! ", e)

start = time.time()


#Decode the Captcha
import cv2
import pytesseract
from PIL import Image
import numpy
import imutils


def CaptchaFind():
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

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    morph2 = cv2.morphologyEx(morph, cv2.MORPH_DILATE, kernel)
    cv2.imwrite("morph.bmp",morph)
    cv2.imwrite("morph2.bmp",morph2)


    text = pytesseract.image_to_string(Image.open("morph.bmp"))
    import re

    regex = re.compile('[^a-zA-Z0-9]')
    text = regex.sub('', text)
    print("text", text)

import sys
if __name__ == "__main__":
    if 1 < len(sys.argv) > 2:
        username = sys.argv[1]
        password = sys.argv[2]
        readurl_captcha(username,password)
    else:
        # readurl_captcha()
        pass
    CaptchaFind()

