from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(800, 600))
display.start()

firefox_opts = webdriver.FirefoxOptions()
firefox_opts.add_argument('--headless')
browser = webdriver.Firefox(firefox_options=firefox_opts)

try:
    # we can now start Firefox and it will run inside the virtual display
    browser = webdriver.Firefox()
    browser.get('http://www.google.com')
    print (browser.title)
    btn = browser.find_element_by_css_selector("div.gb_Q:nth-child(1) > a:nth-child(1)")
    print(btn.text)

finally:
    browser.quit()
    display.stop()