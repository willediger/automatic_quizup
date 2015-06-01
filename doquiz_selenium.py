from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get('https://quizup.com/en/login')

base_window_handle = driver.current_window_handle
print base_window_handle

wait = WebDriverWait(driver, 30)

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

driver.switch_to.window(base_window_handle)

profile_title = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "MyTopics__item")))

driver.get('https://quizup.com/topics/peep-show')

play_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "PlayButton"))).click()

play_random_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "PlayRandomButton"))).click()

question_answers = []
for x in range(1,7):
    question_text = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Question__text")))
    correct_answer = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Answer--correct")))
    question_answers.append([question_text.text, correct_answer])

print question_answers

driver.quit()