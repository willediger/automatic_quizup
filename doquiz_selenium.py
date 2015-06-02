from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import quizupanswers


driver = webdriver.Chrome()
driver.get('https://quizup.com/en/login')

base_window_handle = driver.current_window_handle

wait = WebDriverWait(driver, 200)

while len(driver.window_handles) == 1:
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "FacebookButton"))).click()
    time.sleep(1)

new_window_handle = next(i for i in driver.window_handles if i != base_window_handle)

driver.switch_to.window(new_window_handle)

fb_email = wait.until(EC.element_to_be_clickable((By.ID, "email")))
fb_email.send_keys('willhinsa@gmail.com')

fb_pass = wait.until(EC.element_to_be_clickable((By.ID, "pass")))
fb_pass.send_keys('Dark23@q')

fb_login = wait.until(EC.element_to_be_clickable((By.ID, "loginbutton")))
fb_login.click()

while len(driver.window_handles) > 1:
    time.sleep(1)

driver.switch_to.window(base_window_handle)

profile_title = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "MyTopics__item")))

driver.get("https://quizup.com/topics/peep-show")

play_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "PlayButton")))
time.sleep(1)
play_button.click()

play_random_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "PlayRandomButton")))
time.sleep(1)
play_random_button.click()

question_answers = []
x = 1
while x <= 7:

    round_nbr = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "QuestionScene__round")))
    question = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Question__text")))
    question_text = question.text
    print question_text

    answers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Answer__text")))
    while len(answers[3].text) == 0:
        pass

    answers_text = [i.text for i in answers]
    print '_'.join(answers_text)

    correct_answer = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Answer--correct"))).text
    print correct_answer
    question_answers.append([question_text, correct_answer])

    # curr_question = question_text
    x += 1

driver.quit()

#Answer
#Answer__text