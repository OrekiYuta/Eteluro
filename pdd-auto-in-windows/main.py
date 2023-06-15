import time
# import sys

from selenium import webdriver


def main():
    # Start Chrome Driver
    print("Start Chrome Driver")
    chromedriver = '../chromedriver_win32/chromedriver.exe'
    # executable_path = chromedriver,
    option = webdriver.ChromeOptions()
    option.add_argument("--user-data-dir=" + r"C:/Users/OrekiYuta/AppData/Local/Google/Chrome/User Data/")
    option.add_experimental_option('detach', True)
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=option)  # open chrome

    # Open the URL you want to execute JS
    print("Open the URL you want to execute JS")
    url = 'https://www.pixiv.net/bookmark_new_illust.php'
    driver.get(url)

    # Wait loading full page
    print("Wait loading full page")
    driver.implicitly_wait(30)

    # Execute JS
    driver.execute_script("document.getElementById(\"openCenterPanelBtn\").click();")
    # driver.execute_script("$x(\"/html/div[1]/div[3]/slot/form/div[1]/div/slot[1]/button[1]\")[0].click();")
    driver.execute_script("document.querySelector('html > div.centerWrap.showBlobKeywords.lang_zh-cn > "
                          "div.centerWrap_con.beautify_scrollbar> slot > form > div:nth-child(1) > div > "
                          "slot:nth-child(1) > button:nth-child(1)').click();")

    # Wait for powerful pixiv downloader download finish
    print("Wait for powerful pixiv downloader download finish")
    time.sleep(3700)
    print("All Done")
    driver.quit()

    # sys.exit()

if __name__ == '__main__':
    main()
