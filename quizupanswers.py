import sqlite3

db = sqlite3.connect('answers.db')
db.row_factory = lambda cursor, row: row[0]
c = db.cursor()

# c.execute("select answer from quizup_answers")
# all_rows = c.fetchall()
# print all_rows

# while True:
#     pass

# db.close()

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
    return c.fetchone()


def get_answer(category, question):
    print 'get answer ' + question
    c.execute("select answer "
              "from quizup_answers "
              "where category = ? and question = ?", (category, question,))
    return c.fetchone()

def get_answers(category):
    c.execute("select answer "
              "from quizup_answers "
              "where category = ?", (category,))
    return c.fetchall()



# z = get_category_url('peep-show')
# print z

# db.close()
