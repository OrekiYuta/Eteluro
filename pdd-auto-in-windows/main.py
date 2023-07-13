import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    # 1.Start Chrome Driver
    print("Start Chrome Driver")
    chromedriver = '../chromedriver_win32/chromedriver.exe'
    # executable_path = chromedriver,
    option = webdriver.ChromeOptions()
    option.add_argument("--user-data-dir=" + r"C:/Users/OrekiYuta/AppData/Local/Google/Chrome/User Data/")
    option.add_experimental_option('detach', True)
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=option)  # open chrome

    # 2.Open the URL
    print("Open the URL")
    url: str = 'https://www.pixiv.net/bookmark_new_illust.php'
    driver.get(url)

    # 3.Wait loading full page
    print("Wait loading full page")
    driver.implicitly_wait(30)

    # Execute JS
    # 4.Click to open dialog
    print("Click to open dialog")
    driver.execute_script("document.getElementById(\"openCenterPanelBtn\").click();")

    # 5.Click to open start download
    print("Click to open start download")
    # archive selector in 2023/07/13
    # driver.execute_script("document.querySelector('html > div.centerWrap.showBlobKeywords.lang_zh-cn > "
    #                       "div.centerWrap_con.beautify_scrollbar> slot > form > div:nth-child(1) > div > "
    #                       "slot:nth-child(1) > button:nth-child(1)').click();")

    driver.execute_script("document.querySelector('html > div.centerWrap.showBlobKeywords.lang_zh-cn > "
                          "div.centerWrap_con.beautify_scrollbar > slot > form > div:nth-child(1) > div > "
                          "slot:nth-child(2) > button:nth-child(1)').click();")

    # 6.Wait for powerful pixiv downloader download finish
    print("Wait for powerful pixiv downloader download finish")

    allow_time: int = 3600
    sleep_time: int = 360
    # Limit must end time
    end_time = time.time() + allow_time

    while time.time() < end_time:

        time.sleep(sleep_time)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print("Downloading " + current_time)

        # 7.Check the element to confirm if finish download
        element_down_status = driver.find_element(By.XPATH,
                                                  "/html/div[1]/div[3]/slot/form/div[2]/slot[1]/div/div[2]/span[2]")
        if "完毕" in element_down_status.text:
            print("All Done")
            break

    driver.quit()


if __name__ == '__main__':
    main()
