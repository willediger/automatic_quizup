import sqlite3

db = sqlite3.connect('answers.db')
c = db.cursor()

# db.execute('create table quizup_answers '
#                   '(category text, question text, answer text)')

# db.execute('create table quizup_categories ('
#            'category text, category_url text,'
#            ' primary key (category, category_url))')

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
    return c.fetchone()[0]


def get_answer(category, question):
    c.execute("select answer"
              "from quizup_answers"
              "where category = ? and question = ?", (category, question))
    return c.fetchone()[0]

# z = get_category_url('peep-show')
# print z

# db.close()
