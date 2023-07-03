import time

from selenium import webdriver


def main():
    option = webdriver.ChromeOptions()
    option.add_argument("--user-data-dir=" + r"C:/Users/OrekiYuta/AppData/Local/Google/Chrome/User Data/")
    option.add_experimental_option('detach', True)
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=option)  # open chrome

    url_homepage: str = 'https://www.52pojie.cn/forum.php'
    url_checkin: str = 'https://www.52pojie.cn/home.php?mod=task&do=apply&id=2'
    driver.get(url_homepage)
    time.sleep(3)
    driver.get(url_checkin)
    time.sleep(5)
    driver.quit()


if __name__ == '__main__':
    main()
