import creds, psycopg2, collections, psycopg2.extras


def psql_conn():
    username = creds.psql_login()
    pwd = creds.psql_pwd()
    conn_str = "dbname='quizup' user='{0}' host='localhost' password='{1}'".format(username, pwd)
    conn = psycopg2.connect(conn_str)
    cursor = conn.cursor()
    rich_return = collections.namedtuple('rich', ['conn', 'cursor'])
    r = rich_return(conn, cursor)
    return r

r = psql_conn()
db = r.conn
c = r.cursor

def new_answer(category, question, answer):
    c.execute("insert into quizup_answers values (?,?,?)", (category, question, answer))
    db.commit()


def get_category_url(category_name):
    c.execute("select category_url "
              "from quizup_categories "
              "where category = '{0}'".format(category_name))
    return c.fetchone()


def get_answers(category, question):
    print 'get answers'
    c.execute("select answer "
              "from quizup_answers "
              "where category = '{0}' and question = '{1}'".format(category, question))
    x = c.fetchall()
    c.close()
    return x

def get_questions(category):
    c.execute("select question "
              "from quizup_answers "
              "where category = '{0}'".format(category))
    x = c.fetchall()
    y = [i[0] for i in x]
    c.close()
    return y

x = get_questions("general-knowledge")
print x[0]

#
# try:
#     c.execute("SELECT * from quizup_categories;")
#     c.execute("SELECT * from quizup_categories;")
#     c.execute("SELECT * from quizup_categories;")
#     x = c.fetchall()
#     c.close()
#     print x
# except:
#     print "I am unable to connect to the database"
# finally:
#     db.close()