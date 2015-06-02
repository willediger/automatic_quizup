from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import quizupanswers
import collections

def do_quizup(category_name):
    try:
        login = start_quizup(category_name)
        driver = login.driver
        wait = login.wait
        cycle = cycle_quizup(driver, wait, category_name)
    finally:
        driver.quit()

def cycle_quizup(driver, wait, category_name):
    print 'cycle_quizup'
    while True:
        get_to_category_page(driver, wait, category_name)
        do_questions(driver, wait, category_name)
        # start_next_round(driver, wait, category_name)

# def start_next_round(driver, wait, category_name):
#
#     print 'start_next_round'
#     no_rematch_class = "RematchScene__rematch__button"
#     print no_rematch_class
#     no_rematch = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, no_rematch_class)))
#     print no_rematch
#     time.sleep(1)
#     no_rematch.click()
#     print 'no rematch'
#
#     next_game_play_class = "EndGameResultsActions__button"
#     next_game = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, next_game_play_class)))
#     time.sleep(1)
#     next_game.click()

def start_quizup(category_name):
    print 'start_quizup'
    driver = webdriver.Chrome()
    driver.get('https://quizup.com/en/login')

    base_window_handle = driver.current_window_handle

    wait = WebDriverWait(driver, 200)

    while len(driver.window_handles) == 1:
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "FacebookButton"))).click()
        time.sleep(1)

    new_window_handle = next(i for i in driver.window_handles if i != base_window_handle)

    print 'facebook login open'
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

    print 'facebook logged in'

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "MyTopics__item")))

    rich_return = collections.namedtuple('rich', ['driver', 'wait'])
    r = rich_return(driver, wait)
    return r

def get_to_category_page(driver, wait, category_name):
    print 'get_to_category_page'

    category_url = quizupanswers.get_category_url(category_name)
    driver.get(category_url)

    play_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "PlayButton")))
    time.sleep(1)
    play_button.click()

    print 'clicked play'

    play_random_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "PlayRandomButton")))
    time.sleep(1)
    play_random_button.click()

    print 'clicked play2'


def do_questions(driver, wait, category_name):
    print 'do_questions'
    question_answers = []
    x = 1
    while x <= 7:

        round_nbr = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "QuestionScene__round")))
        print 'round nbr' + str(x)
        question = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Question__text")))
        question_text = question.text

        answer = quizupanswers.get_answer(category_name, question_text)
        print question_text
        print answer

        answers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Answer__text")))
        while len(answers[3].text) == 0:
            pass

        if answer is not None:
            answers_text = [i.text for i in answers]
            correct_answer_idx = answers_text.index(answer)
            answers[correct_answer_idx].click()
        else:
            answers[0].click()

        correct_answer = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Answer--correct"))).text

        if answer is None:
            quizupanswers.new_answer(category_name, question_text, correct_answer)

        print correct_answer
        question_answers.append([question_text, correct_answer])

        x += 1

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "RematchScene__rematch__text")))

    rich_return = collections.namedtuple('rich', ['driver', 'wait'])
    r = rich_return(driver, wait)
    return r
