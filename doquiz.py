import splinter
# from selenium.webdriver.chrome.options import Options
import selenium

browser = splinter.Browser('chrome')

browser.visit('https://quizup.com/en')

#find login button & click it
browser.find_link_by_href('/login')[0].click()

divs = browser.find_by_tag('form')
fb_button = divs[1]
# fb_button = next(i for i in divs if i.text == u'Sign in with Facebook')
fb_button.click()

# chrome_options = Options()
# chrome_options.add_extension('path_to_extension')


# browser.fill('q', 'splinter - python acceptance testing for web applications')
# browser.find_by_name('btnG').click()
#
# if browser.is_text_present('splinter.readthedocs.org'):
#     print "Yes, the official website was found!"
# else:
#     print "No, it wasn't found... We need to improve our SEO techniques"

# browser.quit()