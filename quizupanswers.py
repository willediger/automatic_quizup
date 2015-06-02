import sqlite3

answer_db = sqlite3.connect('answers.db')

answer_db.execute('create table quizup_answers '
                  '(category text, question text, answer text)')
