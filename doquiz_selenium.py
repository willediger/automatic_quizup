from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://quizup.com/en/login')

wait = WebDriverWait(driver, 10)

def elem_clickable(WebDriverWait,ByType,ByText):
    return wait.until(EC.presence_of_all_elements_located((ByType, ByText)))

fb_button = elem_clickable(wait, By.CLASS_NAME,'FacebookButton')[0]

fb_button.click()



driver.switch_to.window('Facebook')


fb_email = elem_clickable(wait, By.ID,'email')[0]

fb_email.send_keys('willhinsa@gmail.com')

# id = email
# id = pass
# id = persist_box ; value = 1

driver.close()
