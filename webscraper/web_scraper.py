from selenium import webdriver

driver = webdriver.Firefox()

driver.get('https://imslp.org/wiki/Category:Composers')

menu = driver.find_element_by_id('bs-top-navbar')


print(composer_link)
