from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
driver.get('https://quizup.com/en/login')

base_window_handle = driver.current_window_handle
print base_window_handle

wait = WebDriverWait(driver, 10)

while len(driver.window_handles) == 1:
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "FacebookButton"))).click()
    time.sleep(1)

new_window_handle = next(i for i in driver.window_handles if i != base_window_handle)
print new_window_handle

driver.switch_to.window(new_window_handle)

fb_email = wait.until(EC.element_to_be_clickable((By.ID, "email")))
fb_email.send_keys('willhinsa@gmail.com')

fb_pass = wait.until(EC.element_to_be_clickable((By.ID, "pass")))
fb_pass.send_keys('Dark23@q')

fb_login = wait.until(EC.element_to_be_clickable((By.ID, "loginbutton")))
fb_login.click()

while len(driver.window_handles) > 1:
    time.sleep(1)

print driver.window_handles

driver.switch_to(base_window_handle)
# driver.get('https://quizup.com/topics/peep-show')

driver.quit()

# fb_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.CLASS_NAME,'FacebookButton'))

# fb_button = elem_clickable(wait, By.CLASS_NAME,'FacebookButton')[0]
# driver.implicitly_wait(5)

# element.click()
# driver.implicitly_wait(5)
#
# driver.switch_to.window('Facebook')
#
#


# id = email
# id = pass
# id = persist_box ; value = 1



element.click()


windows = driver.switch_to.window()

driver.close()
