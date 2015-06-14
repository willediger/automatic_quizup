from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import quizupanswers
import collections
import random
import time
import datetime
from timeout import timeout
import creds
import psycopg2



def psql_conn():
    username = creds.psql_login()
    pwd = creds.psql_pwd()
    conn_str = "dbname='quizup' user='{0}' host='localhost' password='{1}'".format(username, pwd)
    conn = psycopg2.connect(conn_str)
    cursor = conn.cursor()

def do_quizup(category_name):
    print 'do quizup'
    driver = create_driver()

    try:
        login = start_quizup(driver, category_name)
        wait = login.wait
        cycle_quizup(driver, wait, category_name)
    except:
        print 'failed cycle'
        # z = login.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "EndGameHeader__results__text")))
        # print z.text
    finally:
        driver.quit()

    # login = start_quizup(driver, category_name)
    # wait = login.wait
    # cycle_quizup(driver, wait, category_name)


def create_driver():
    print 'create_driver'
    driver = webdriver.Chrome()
    return driver


def login(type, driver, wait, base_window_handle):
    if type == "Facebook":

        fb_username = creds.fb_login()
        fb_pwd = creds.fb_pwd()

        while len(driver.window_handles) == 1:
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "FacebookButton"))).click()
            time.sleep(1)

        new_window_handle = next(i for i in driver.window_handles if i != base_window_handle)
        print 'facebook login open'
        driver.switch_to.window(new_window_handle)

        fb_email = wait.until(EC.element_to_be_clickable((By.ID, "email")))
        fb_email.send_keys(fb_username)

        fb_pass = wait.until(EC.element_to_be_clickable((By.ID, "pass")))
        fb_pass.send_keys(fb_pwd)

        fb_login = wait.until(EC.element_to_be_clickable((By.ID, "loginbutton")))
        fb_login.click()

        while len(driver.window_handles) > 1:
            time.sleep(1)

        print 'facebook logged in'

    elif type == "Google":

        google_username = creds.google_login()
        google_pwd = creds.google_pwd()

        while len(driver.window_handles) == 1:
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "GoogleButton"))).click()
            time.sleep(1)

        new_window_handle = next(i for i in driver.window_handles if i != base_window_handle)
        print 'google login open'
        driver.switch_to.window(new_window_handle)

        email = wait.until(EC.element_to_be_clickable((By.ID, "Email")))
        email.send_keys(google_username)

        next_btn = wait.until(EC.element_to_be_clickable((By.ID, "next")))
        next_btn.click()

        passwd = wait.until(EC.element_to_be_clickable((By.ID, "Passwd")))
        passwd.send_keys(google_pwd)

        login = wait.until(EC.element_to_be_clickable((By.ID, "signIn")))
        login.click()

        while len(driver.window_handles) > 1:
            time.sleep(1)

        print 'Google logged in'

@timeout(60)
def start_quizup(driver, category_name):
    print 'start_quizup'
    driver.get('https://quizup.com/en/login')

    base_window_handle = driver.current_window_handle

    wait = WebDriverWait(driver, 60)

    # login("Facebook", driver, wait, base_window_handle)
    print 'login'
    login("Google", driver, wait, base_window_handle)

    driver.switch_to.window(base_window_handle)

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "MyTopics__item")))

    rich_return = collections.namedtuple('rich', ['driver', 'wait'])
    r = rich_return(driver, wait)
    print 'DONE - start_quizup'
    return r


def cycle_quizup(driver, wait, category_name):
    print 'cycle_quizup'
    while True:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print st
        get_to_category_page(driver, wait, category_name)
        do_questions(driver, wait, category_name)


@timeout(60)
def get_to_category_page(driver, wait, category_name):
    print 'get_to_category_page'

    category_url = quizupanswers.get_category_url(category_name)
    driver.get(category_url)

    print 'navigating to category page'

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ContactList__items")))
    print 'contact list loaded'

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "PlayButton__icon")))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Story")))

    print 'play button icon loaded'
    play_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "PlayButton")))
    time.sleep(3)
    play_button.click()

    print 'clicked play'

    play_random_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "PlayRandomButton")))
    time.sleep(3)
    play_random_button.click()

    print 'clicked play2'

def get_question(wait):
    question = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Question__text")))
    return question


@timeout(300)
def do_questions(driver, wait, category_name):
    print 'do_questions'
    question_answers = []
    x = 1
    prev_question = u''
    question_text = u''
    while x <= 7:
        while prev_question == question_text or question_text == u'':
            question = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Question__text")))
            try:
                question_text = question.text
            except:
                # try:
                #     wait.until(EC.presence_of_element_located((By.CLASS_NAME, "EndGameHeader__results__text")))
                #     break

                question_text = u''

        print 'round nbr' + str(x)

        stored_answers = quizupanswers.get_answers(category_name, question_text)
        print question_text
        print stored_answers

        answers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Answer__text")))
        while len(answers[3].text) == 0:
            pass

        answers_text = [i.text for i in answers]
        print answers_text

        guess_idx = random.randint(0,3)
        if stored_answers:
            try:
                correct_stored_answer = list(set(stored_answers) & set(answers_text))[0]
                correct_answer_idx = answers_text.index(correct_stored_answer)
                answers[correct_answer_idx].click()
            except:
                stored_answers = []
                answers[guess_idx].click()
        else:
            answers[guess_idx].click()

        correct_answer = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Answer--correct"))).text

        if not stored_answers:
            quizupanswers.new_answer(category_name, question_text, correct_answer)

        print correct_answer
        question_answers.append([question_text, correct_answer])

        prev_question = question_text

        x += 1

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "RematchScene__rematch__text")))

    rich_return = collections.namedtuple('rich', ['driver', 'wait'])
    r = rich_return(driver, wait)
    return r

