import sqlite3

def new_category(db, c, category_name, category_url):
    c.execute("insert into quizup_categories values (?,?)", (category_name, category_url))
    db.commit()

