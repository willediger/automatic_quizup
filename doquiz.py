import doquiz_selenium

# category = 'peep-show'
category = 'general-knowledge'

while True:
    try:
        doquiz_selenium.do_quizup(category)
    except:
        'do_quizup failed'
        doquiz_selenium.do_quizup(category)

# doquiz_selenium.do_quizup(category)