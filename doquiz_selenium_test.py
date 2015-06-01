from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

driver = webdriver.Chrome()
driver.get("https://quizup.com/en/login")
element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'FacebookButton')))


element.click()

print driver.window_handles
driver.close()