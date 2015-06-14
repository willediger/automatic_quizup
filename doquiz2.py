from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import collections
import random
import time, threading, traceback, sys
from selenium.webdriver.common.keys import Keys
import db_answers

import sqlite3


threadLock = threading.Lock()


def do_quizup(url, category_name):

    driver = create_driver(url)

    try:
        login = start_quizup(driver)
        wait = login.wait
        cycle_quizup(driver, wait, category_name)
    except Exception, e:
        threadLock.acquire()
        print "Unexpected error encountered while running test."
        traceback.print_exc(file=sys.stdout)
        threadLock.release()
    finally:
        driver.quit()

def create_driver(url):
    driver = webdriver.Remote(url, webdriver.DesiredCapabilities.CHROME)
    return driver


def start_quizup(driver):
    driver.get('https://quizup.com/en/login')

    base_window_handle = driver.current_window_handle

    wait = WebDriverWait(driver, 60)

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

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "MyTopics__item")))

    rich_return = collections.namedtuple('rich', ['driver', 'wait'])
    r = rich_return(driver, wait)
    return r


def cycle_quizup(driver, wait, category_name):
    db = create_db()
    c = db.cursor()
    while True:
        get_to_category_page(driver, wait, category_name, c)
        do_questions(driver, wait, category_name, db, c)
    db.close()


def get_to_category_page(driver, wait, category_name, c):

    category_url = db_answers.get_category_url(c, category_name)
    driver.get(category_url)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ContactList__items")))

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "PlayButton__icon")))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Story")))

    play_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "PlayButton")))
    time.sleep(3)
    play_button.click()

    play_random_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "PlayRandomButton")))
    time.sleep(3)
    play_random_button.click()

def get_question(wait):
    question = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Question__text")))
    return question

def do_questions(driver, wait, category_name, db, c):
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

        stored_answers = db_answers.get_answers(db, c, category_name, question_text)

        answers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Answer__text")))
        while len(answers[3].text) == 0:
            pass

        answers_text = [i.text for i in answers]

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
            db_answers.new_answer(db, c, category_name, question_text, correct_answer)

        question_answers.append([question_text, correct_answer])

        prev_question = question_text

        x += 1

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "RematchScene__rematch__text")))

    rich_return = collections.namedtuple('rich', ['driver', 'wait'])
    r = rich_return(driver, wait)
    return r


def create_db():
    db = sqlite3.connect('answers.db')
    db.row_factory = lambda cursor, row: row[0]
    return db


def new_answer(db, c,  category, question, answer):
    c.execute("insert into quizup_answers values (?,?,?)", (category, question, answer))
    db.commit()


def get_category_url(c, category_name):
    c.execute("select category_url "
              "from quizup_categories "
              "where category = ?", (category_name,))
    return c.fetchone()


def get_answers(c, category, question):
    c.execute("select answer "
              "from quizup_answers "
              "where category = ? and question = ?", (category, question,))
    return c.fetchall()



def main():
  maxRequestsPerHost = 2
  hosts = ["localhost:8080"]
  categories = [ "quiz-up", "quiz-up" ] #, "quiz-up", "quiz-up"

  if len(hosts) == 0:
    return

  reqs = []
  for idx, host in enumerate(hosts):
    first = idx*maxRequestsPerHost
    last = idx*maxRequestsPerHost+maxRequestsPerHost
    for category in categories[first:last]:
        url = str.format("http://{0}/wd/hub", host)
        reqs.append([url, category])

  threads = []
  for req in reqs:
    thread = threading.Thread(target=do_quizup, args=[req[0], req[1]])
    thread.start()
    threads.append(thread)

  for t in threads:
    t.join()


if __name__== "__main__":
    main()

