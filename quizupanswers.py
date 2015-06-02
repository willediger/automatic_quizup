import sqlite3

db = sqlite3.connect('answers.db')

# db.execute('create table quizup_answers '
#                   '(category text, question text, answer text)')



db.close()
