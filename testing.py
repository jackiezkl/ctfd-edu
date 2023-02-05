from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time,random

firefoxoptions = Options()
firefoxoptions.add_argument("--headless")

with webdriver.Firefox(options=firefoxoptions) as driver:
  driver.get("http://127.0.0.1")
  for i in range(1,20):
    driver.find_element(By.XPATH,"/html/body/nav/div/div/ul[2]/li[1]/a").click()
    driver.find_element(By.XPATH,'//*[@id="name"]').send_keys(f"test{i}")
    driver.find_element(By.XPATH,'//*[@id="email"]').send_keys(f"test{i}@gmail.com")
    driver.find_element(By.XPATH,'//*[@id="password"]').send_keys("passtest")
    driver.find_element(By.XPATH,'//*[@id="fields[1]"]').send_keys(f"first{i} last{i}")
    driver.find_element(By.XPATH,f'/html/body/main/div[2]/div/div/form/div[5]/select/option[{random.randint(2,13)}]').click()
    driver.find_element(By.XPATH,'//*[@id="_submit"]').click()
    time.sleep(1.5)
    driver.find_element(By.XPATH,'/html/body/nav/div/div/ul[2]/li[4]/a/span[2]/i').click()
    time.sleep(1.5)
    print(f"user test{i} added")
