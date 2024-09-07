# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

links = [
    ['pinterest-men','https://www.pinterest.com/Marcellthekid/men-fashion-catalog/'],
    ['pinterest-women',"https://www.pinterest.com/Kuricho/womens-t-shirts/"],
    ['vogue-fashion','https://www.vogue.in/fashion/fashion-trends']
]
option = 2

driver = webdriver.Chrome(executable_path="chromedriver")

#open the webpage
driver.get(links[option][1])

driver.execute_script("window.scrollTo(0, 4000);")
images = driver.find_elements(by=By.TAG_NAME, value='img')
images = [image.get_attribute('src') for image in images]
images[:-2]

import os
import wget

path = os.getcwd()

counter = 0
for image in images:
    save_as = os.path.join(path+'/current-fashion', links[option][0]  + str(counter) + '.jpg')
    wget.download(image, save_as)
    counter += 1

