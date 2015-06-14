import sqlite3

db = sqlite3.connect('answers.db')
db.row_factory = lambda cursor, row: row[0]
c = db.cursor()


def new_category(category_name, category_url):
    c.execute("insert into quizup_categories values (?,?)", (category_name, category_url))
    db.commit()


def new_answer(category, question, answer):
    c.execute("insert into quizup_answers values (?,?,?)", (category, question, answer))
    db.commit()


def get_category_url(category_name):
    c.execute("select category_url "
              "from quizup_categories "
              "where category = ?", (category_name,))
    return c.fetchone()


def get_answer(category, question):
    print 'get answer'
    c.execute("select answer "
              "from quizup_answers "
              "where category = ? and question = ?", (category, question,))
    return c.fetchone()

def get_answers(category, question):
    print 'get answers'
    c.execute("select answer "
              "from quizup_answers "
              "where category = ? and question = ?", (category, question,))
    return c.fetchall()
